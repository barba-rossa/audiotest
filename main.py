import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os

# Carrega o modelo (isso pode demorar na primeira vez)
model = whisper.load_model("base")

def transcrever_audio():
    filepath = filedialog.askopenfilename(
        filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.m4a *.flac *.ogg *.webm")]
    )
    
    if not filepath:
        return

    try:
        transcricao_texto.set("Processando...")
        root.update()

        resultado = model.transcribe(filepath)
        texto = resultado["text"]

        # Mostra na interface
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, texto)

        # Salva em arquivo .txt
        nome_arquivo = os.path.splitext(os.path.basename(filepath))[0]
        with open(f"{nome_arquivo}_transcricao.txt", "w", encoding="utf-8") as f:
            f.write(texto)

        transcricao_texto.set("Transcrição completa!")
        messagebox.showinfo("Sucesso", "Transcrição salva com sucesso.")
    except Exception as e:
        transcricao_texto.set("Erro!")
        messagebox.showerror("Erro", str(e))


# GUI Tkinter
root = tk.Tk()
root.title("Transcritor de Áudio com Whisper")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=20)

botao = tk.Button(frame, text="Selecionar Áudio e Transcrever", command=transcrever_audio, font=("Arial", 12))
botao.pack()

transcricao_texto = tk.StringVar()
transcricao_texto.set("Nenhuma transcrição ainda.")
label = tk.Label(root, textvariable=transcricao_texto, font=("Arial", 10))
label.pack()

text_box = tk.Text(root, height=15, wrap=tk.WORD)
text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
