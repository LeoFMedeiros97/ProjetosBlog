"""Executa uma análise local com o Python da .venv da raiz. Não é um sandbox."""

import os
import shutil
import signal
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

PYTHON = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "python"


def executar_codigo(codigo: str, dados: Path, resultados: Path, timeout: int = 30) -> dict:
    if not PYTHON.is_file():
        raise FileNotFoundError("Crie a .venv na raiz e instale as dependências do Projeto02.")
    if not codigo.strip() or len(codigo) > 20_000:
        raise ValueError("Envie um código Python entre 1 e 20.000 caracteres.")

    # Cada execução tem sua própria pasta, preservando os resultados anteriores.
    pasta = resultados / f"python_{uuid4().hex[:8]}"
    pasta.mkdir(parents=True)
    (pasta / "codigo.py").write_text(codigo, encoding="utf-8")

    with TemporaryDirectory(prefix="projeto02_") as temporario:
        temporario = Path(temporario)
        for nome in ("fundamentos.csv", "precos.csv"):
            original = dados / nome
            if original.is_file():
                shutil.copyfile(original, temporario / nome)

        # O código recebe uma cópia dos dados e bibliotecas prontas para usar.
        preparacao = (
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n"
            f"pasta_dados = Path({str(temporario)!r})\n"
            "fundamentos = pd.read_csv(pasta_dados / 'fundamentos.csv') if (pasta_dados / 'fundamentos.csv').exists() else pd.DataFrame()\n"
            "precos = pd.read_csv(pasta_dados / 'precos.csv', index_col='data', parse_dates=True) if (pasta_dados / 'precos.csv').exists() else pd.DataFrame()\n"
        )
        script = temporario / "analise.py"
        script.write_text(preparacao + "\n" + codigo, encoding="utf-8")

        # Não herdamos OPENAI_API_KEY nem outras variáveis do processo do agente.
        ambiente = {
            "PATH": str(PYTHON.parent) + os.pathsep + os.defpath,
            "HOME": str(temporario),
            "MPLCONFIGDIR": str(temporario / "matplotlib"),
            "TMPDIR": str(temporario),
            "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
        }
        # A saída vai para um arquivo temporário para não encher a memória do agente.
        with (temporario / "saida.txt").open("w+", encoding="utf-8") as saida:
            processo = subprocess.Popen(
                [str(PYTHON), "-I", "-u", str(script)],
                cwd=pasta, env=ambiente, stdout=saida, stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                processo.wait(timeout=timeout)
                status = "ok" if processo.returncode == 0 else "erro"
            except subprocess.TimeoutExpired:
                status = "tempo_esgotado"
            finally:
                # Encerra também subprocessos comuns iniciados pela análise.
                try:
                    os.killpg(processo.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                processo.wait()
            saida.seek(0)
            texto = saida.read(12_000)
            if saida.read(1):
                texto += "\n[Saída truncada em 12.000 caracteres.]"

    return {
        "status": status,
        "saida": texto,
        "pasta": str(pasta),
        "arquivos": sorted(item.name for item in pasta.iterdir()
                           if item.is_file() and not item.is_symlink()),
    }
