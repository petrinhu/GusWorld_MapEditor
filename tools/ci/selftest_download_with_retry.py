#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/selftest_download_with_retry.py

Autoteste de download_with_retry.py com QUATRO controles:

    1. SUCESSO IMEDIATO -- servidor responde 200 de primeira, prova o
       caminho feliz (exit 0, arquivo gravado com o conteudo certo).
    2. REPETICAO DE VERDADE -- servidor falha (500) nas duas primeiras
       chamadas e responde 200 na terceira; prova que o script REPETE de
       verdade contra uma falha de rede REAL (nao um mock de funcao) e
       entrega o conteudo certo depois de duas falhas.
    3. FALHA DEFINITIVA -- servidor falha (500) em TODAS as chamadas
       dentro do numero de tentativas configurado; prova que o script
       desiste no numero certo de tentativas, sai 1, nao deixa arquivo
       parcial, e a mensagem de erro tem o prefixo "REDE" e o texto
       "falha definitiva" -- nunca mencionando checksum ou gitleaks, para
       nao criar ambiguidade com as outras duas causas reais de vermelho.
    4. BACKOFF CRESCENTE -- chama a funcao Python direto (injetando
       `dormir` para nao esperar de verdade) contra um endereco que falha
       na hora (porta sem listener) e prova que a sequencia de esperas
       dobra a cada tentativa (base, 2*base, 4*base, ...), o numero de
       esperas bate com o numero de falhas (uma a menos que o numero de
       tentativas: nao ha espera depois da ULTIMA tentativa fracassada).

Roda os controles 1-3 via subprocess contra um servidor HTTP real em
localhost (thread deste processo), porque o que precisa ser provado e o
comportamento OBSERVAVEL do script tal como o workflow do GitHub Actions
vai invoca-lo -- e o controle 2 so prova algo se a falha for uma falha de
rede EFETIVA (requisicao HTTP que de fato retornou erro), nao um dublê de
funcao.

Uso:
    python3 tools/ci/selftest_download_with_retry.py

Exit 0 = os quatro controles se comportaram como esperado.
Exit 1 = pelo menos um controle falhou (o script real tem um defeito).
"""
from __future__ import annotations

import http.server
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "download_with_retry.py"

sys.path.insert(0, str(SCRIPT.parent))
import download_with_retry  # noqa: E402


class _ContadorHandler(http.server.BaseHTTPRequestHandler):
    """Handler de teste: falha as primeiras `falhas_antes_do_sucesso`
    chamadas com HTTP 500, depois responde 200 com corpo fixo."""

    falhas_antes_do_sucesso = 0
    corpo = b"conteudo-de-teste"
    contador = 0
    lock = threading.Lock()

    def do_GET(self):  # noqa: N802 -- nome exigido pela stdlib (BaseHTTPRequestHandler)
        with _ContadorHandler.lock:
            _ContadorHandler.contador += 1
            numero = _ContadorHandler.contador
        if numero <= _ContadorHandler.falhas_antes_do_sucesso:
            self.send_response(500)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Length", str(len(_ContadorHandler.corpo)))
        self.end_headers()
        self.wfile.write(_ContadorHandler.corpo)

    def log_message(self, format, *args):  # silencia o log padrao do http.server
        pass


def _subir_servidor(falhas_antes_do_sucesso: int):
    _ContadorHandler.falhas_antes_do_sucesso = falhas_antes_do_sucesso
    _ContadorHandler.contador = 0
    servidor = http.server.HTTPServer(("127.0.0.1", 0), _ContadorHandler)
    porta = servidor.server_address[1]
    fio = threading.Thread(target=servidor.serve_forever, daemon=True)
    fio.start()
    return servidor, fio, porta


def _rodar_script(
    url: str, destino: Path, max_tentativas: int, espera_base_seg: float
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable, str(SCRIPT), url, str(destino),
            "--max-tentativas", str(max_tentativas),
            "--espera-base-seg", str(espera_base_seg),
            "--timeout-seg", "5",
        ],
        capture_output=True, text=True,
    )


def control_sucesso_imediato() -> tuple[bool, str]:
    servidor, fio, porta = _subir_servidor(falhas_antes_do_sucesso=0)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "saida.bin"
            r = _rodar_script(
                f"http://127.0.0.1:{porta}/x", destino,
                max_tentativas=3, espera_base_seg=0.05,
            )
            if r.returncode != 0:
                return False, f"esperava exit 0, saiu {r.returncode}. stdout={r.stdout!r} stderr={r.stderr!r}"
            if not destino.exists() or destino.read_bytes() != _ContadorHandler.corpo:
                return False, "arquivo nao foi gravado com o conteudo esperado"
            if "REDE: sucesso na tentativa 1/3" not in r.stdout:
                return False, f"log nao confirma sucesso na 1a tentativa: {r.stdout!r}"
            return True, "ok"
    finally:
        servidor.shutdown()
        fio.join(timeout=2)


def control_repeticao_de_verdade() -> tuple[bool, str]:
    servidor, fio, porta = _subir_servidor(falhas_antes_do_sucesso=2)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "saida.bin"
            r = _rodar_script(
                f"http://127.0.0.1:{porta}/x", destino,
                max_tentativas=5, espera_base_seg=0.05,
            )
            if r.returncode != 0:
                return False, f"esperava exit 0 apos repetir, saiu {r.returncode}. stdout={r.stdout!r} stderr={r.stderr!r}"
            if destino.read_bytes() != _ContadorHandler.corpo:
                return False, "conteudo final nao bate apos repeticao"
            if _ContadorHandler.contador != 3:
                return False, (
                    f"esperava exatamente 3 chamadas ao servidor (2 falhas + 1 sucesso), "
                    f"houve {_ContadorHandler.contador}"
                )
            if (
                "tentativa 1/5" not in r.stdout
                or "tentativa 2/5" not in r.stdout
                or "sucesso na tentativa 3/5" not in r.stdout
            ):
                return False, f"log nao mostra a sequencia esperada de tentativas: {r.stdout!r}"
            return True, "ok"
    finally:
        servidor.shutdown()
        fio.join(timeout=2)


def control_falha_definitiva() -> tuple[bool, str]:
    servidor, fio, porta = _subir_servidor(falhas_antes_do_sucesso=999)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "saida.bin"
            r = _rodar_script(
                f"http://127.0.0.1:{porta}/x", destino,
                max_tentativas=3, espera_base_seg=0.05,
            )
            if r.returncode != 1:
                return False, f"esperava exit 1, saiu {r.returncode}. stdout={r.stdout!r} stderr={r.stderr!r}"
            if destino.exists():
                return False, "nao deveria ter gravado arquivo nenhum apos falha definitiva"
            if "REDE" not in r.stderr or "falha definitiva" not in r.stderr:
                return False, f"mensagem de falha definitiva sem o prefixo esperado: {r.stderr!r}"
            # A mensagem PODE citar "checksum" e "gitleaks" -- mas so na forma
            # de negacao explicita ("NAO e checksum nem achado do gitleaks"),
            # que e a disambiguacao pedida. O que e proibido e a mensagem
            # AFIRMAR (sem negar) que o problema e checksum ou achado real.
            if "nao e checksum" not in r.stderr.lower() and "não e checksum" not in r.stderr.lower():
                return False, (
                    f"mensagem de falha de rede nao deixa explicito que NAO e "
                    f"checksum nem achado do gitleaks: {r.stderr!r}"
                )
            if _ContadorHandler.contador != 3:
                return False, f"esperava exatamente 3 tentativas, houve {_ContadorHandler.contador}"
            return True, "ok"
    finally:
        servidor.shutdown()
        fio.join(timeout=2)


def control_backoff_crescente() -> tuple[bool, str]:
    esperas: list[float] = []

    def dormir_falso(segundos: float) -> None:
        esperas.append(segundos)

    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "saida.bin"
        codigo = download_with_retry.baixar_com_repeticao(
            url="http://127.0.0.1:1/inexistente-de-proposito",
            destino=str(destino),
            max_tentativas=4,
            espera_base_seg=3.0,
            timeout_seg=1.0,
            dormir=dormir_falso,
        )
    if codigo != 1:
        return False, f"esperava exit 1 (endereco sempre falha), saiu {codigo}"
    if esperas != [3.0, 6.0, 12.0]:
        return False, f"esperava backoff [3.0, 6.0, 12.0] (3 esperas para 4 tentativas), obteve {esperas}"
    return True, "ok"


CONTROLES = [
    ("sucesso imediato", control_sucesso_imediato),
    ("repeticao de verdade (2 falhas reais + sucesso)", control_repeticao_de_verdade),
    ("falha definitiva (rede sempre fora, nao confundir com checksum/gitleaks)", control_falha_definitiva),
    ("backoff cresce e para no numero certo de vezes", control_backoff_crescente),
]


def main() -> int:
    ok_geral = True
    for nome, funcao in CONTROLES:
        ok, detalhe = funcao()
        status = "PASSOU" if ok else "FALHOU"
        print(f"[{status}] {nome}: {detalhe}")
        ok_geral = ok_geral and ok
    if ok_geral:
        print(f"selftest_download_with_retry: {len(CONTROLES)}/{len(CONTROLES)} controles OK")
        return 0
    print("selftest_download_with_retry: FALHA -- ver detalhe acima", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
