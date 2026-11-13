import struct

MAGIC = b"WSTR"

def pack(path):
    try:
        # reads path
        dados = path.read_bytes()
        nome = path.name.encode()

        # cleans extra junk, so it doesnt forget file name
        header = MAGIC + struct.pack(">BI", len(nome), len(dados)) + nome
        return header + dados
    except AttributeError as e:
        raise AttributeError(f"inserted input isnt a path: {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"no such file:  {e}")

def unpack(blob):
    if len(blob) < 9:
        raise ValueError("this isnt one of ours")
    if blob[:4] != MAGIC:
        raise ValueError("this isnt one of ours")

    nome_len, dados_len = struct.unpack(">BI", blob[4:9])
    nome = blob[9 : 9 + nome_len].decode()
    dados = blob[9 + nome_len : 9 + nome_len + dados_len]

    if len(dados) != dados_len:
        raise ValueError("this file got cut off")
    return nome, dados


if __name__ == "__main__":
    from pathlib import Path

    original = Path("pack.py") # makes path object
    blob = pack(original) # returns the blob
    nome, dados = unpack(blob) # returns name and data

    # checks for bug cases or undefined behaviour
    assert nome == original.name, "name came back diferent"
    assert dados == original.read_bytes(), "data came back different"
    print("round trip ok", len(dados), "bytes")
