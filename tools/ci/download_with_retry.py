#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/download_with_retry.py

Baixa um arquivo por HTTP(S) com repeticao e espera crescente (backoff
exponencial), para tolerar falha TRANSITORIA de rede sem esconder falha
REAL de conteudo (checksum) ou achado real (gitleaks).

Motivacao (medida em 23/08/2026): o job "gitleaks (secrets no historico)"
falhou com "curl: (35) Recv failure: Connection reset by peer" ao baixar o
binario do gitleaks das releases do GitHub. Nao foi vazamento nem defeito
de codigo -- foi a rede que caiu no meio do download, e reexecutar o job
resolveu na hora. Um portao vermelho por causa de rede bloqueia push
(GODS_LAWS.md L-17) por um motivo que nao tem nada a ver com o codigo, e
ensina a reexecutar CI vermelho sem ler -- o habito que a L-09 existe para
combater.

Uso:
    python3 tools/ci/download_with_retry.py <url> <destino>
        [--max-tentativas N]    default 5 (numero de tentativas TOTAIS,
                                 nao numero de repeticoes)
        [--espera-base-seg N]   default 5 -- a espera dobra a cada
                                 tentativa: 5, 10, 20, 40, ... segundos
        [--timeout-seg N]       default 30 -- timeout de socket por
                                 tentativa

Nenhum numero aqui e magico: os tres sao parametro de linha de comando com
default explicito nesta docstring, nunca literal solto no meio do codigo.

Contrato de saida:
    - Sucesso: exit 0, arquivo escrito em <destino> por inteiro (nunca
      parcial -- grava so depois de ler a resposta inteira), log
      prefixado "REDE:".
    - Falha apos esgotar as tentativas: exit 1, log prefixado
      "REDE (falha definitiva apos N tentativas, NAO e checksum nem
      achado do gitleaks): ..." em stderr. O prefixo existe para que quem
      le o resumo do job distinga isto das outras duas causas reais de
      vermelho (checksum nao confere, segredo encontrado), que sao passos
      SEPARADOS deste script e usam outro prefixo cada um.

Este script SO baixa e grava bytes cru. Ele NAO verifica checksum -- essa
verificacao continua obrigatoria, continua podendo derrubar o job, e e
feita pelo step que chama este script. Checksum errado NUNCA deve ser
tratado como falha de rede nem repetido: o binario esta errado, repetir o
download do mesmo binario errado nao conserta nada.
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request


def baixar_com_repeticao(
    url: str,
    destino: str,
    max_tentativas: int,
    espera_base_seg: float,
    timeout_seg: float,
    dormir=time.sleep,
) -> int:
    """Baixa `url` para `destino`, repetindo em falha de rede.

    `dormir` e injetavel para autoteste (evita esperar de verdade a espera
    exponencial real durante o autoteste deste script).
    """
    espera = espera_base_seg
    for tentativa in range(1, max_tentativas + 1):
        print(
            f"REDE: tentativa {tentativa}/{max_tentativas} -- baixando {url}",
            flush=True,
        )
        try:
            with urllib.request.urlopen(url, timeout=timeout_seg) as resposta:
                dados = resposta.read()
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            ConnectionError,
            OSError,
        ) as erro:
            if tentativa >= max_tentativas:
                print(
                    f"REDE (falha definitiva apos {max_tentativas} tentativas, "
                    f"NAO e checksum nem achado do gitleaks): {url} -- {erro!r}",
                    file=sys.stderr,
                    flush=True,
                )
                return 1
            print(
                f"REDE: falha na tentativa {tentativa}/{max_tentativas} ({erro!r}) "
                f"-- esperando {espera:.0f}s antes de repetir",
                flush=True,
            )
            dormir(espera)
            espera *= 2
            continue

        # So grava depois de ter a resposta inteira em memoria: nunca deixa
        # um arquivo parcial no destino em caso de corte no meio da leitura.
        with open(destino, "wb") as arquivo:
            arquivo.write(dados)
        print(
            f"REDE: sucesso na tentativa {tentativa}/{max_tentativas} -- "
            f"{url} ({len(dados)} bytes)",
            flush=True,
        )
        return 0

    return 1


def main(argv: list[str] | None = None) -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument("url")
    analisador.add_argument("destino")
    analisador.add_argument("--max-tentativas", type=int, default=5)
    analisador.add_argument("--espera-base-seg", type=float, default=5.0)
    analisador.add_argument("--timeout-seg", type=float, default=30.0)
    args = analisador.parse_args(argv)

    if args.max_tentativas < 1:
        print("REDE: --max-tentativas precisa ser >= 1", file=sys.stderr)
        return 2

    return baixar_com_repeticao(
        args.url,
        args.destino,
        args.max_tentativas,
        args.espera_base_seg,
        args.timeout_seg,
    )


if __name__ == "__main__":
    raise SystemExit(main())
