from audiocraft.models import MusicGen
import torchaudio
print("Loading model...")
model = MusicGen.get_pretrained("facebook/musicgen-small")
prompt = ["relaxing piano meditation music"]
wav = model.generate(prompt)
torchaudio.save("output.wav", wav[0].cpu(), 32000)
print("Music generated: output.wav")