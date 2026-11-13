import wave as w


def encode(blob, out):
    file = w.open(str(out), "wb")

    # setup
    file.setnchannels(1)
    file.setsampwidth(1)
    file.setframerate(8000)

    file.writeframes(blob)

    file.close()

def decode(path):
    read = w.open(str(path), "rb")

    frames = read.getnframes()
    frames_read = read.readframes(frames)

    read.close()

    return frames_read


if __name__ == "__main__":
    from pathlib import Path

    from pack import pack, unpack


    original = Path("pack.py") # makes path object
    out = Path("test.wav")

    blob = pack(original) # returns the blob
    encode(blob, out)
    nome, dados = unpack(decode(out)) # returns name and data

    # checks for bug cases or undefined behaviour
    assert nome == original.name, "name came back diferent"
    assert dados == original.read_bytes(), "data came back different"
    print("round trip ok", len(dados), "bytes")
