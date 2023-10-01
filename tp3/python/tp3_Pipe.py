import multiprocessing

def father():
    send, recive = multiprocessing.Pipe()

    process = multiprocessing.Process(target=child, args=(send, recive))
    process.start()

    end_process = False
    while end_process == False:
        text = input("Ingrese el texto a procesar: ").split()
        for word in text:
            if word != "close":
                send.send(word)
            else:
                end_process = True;
                break;

    send.send("close")
    process.join()
    if recive.poll():
        stats = recive.recv()
        print("Cantidad de caracteres totales: ", stats["total_length"])
        print("Cantidad de letras: ", stats["total_letters"])
        print("Cantidad de dígitos: ", stats["total_digits"])
        print("La palabra de mayor longitud: ", stats["longest_word"])
        print("La palabra de menor longitud: ", stats["shortest_word"])
        
    send.close()
    recive.close()

def child(send_pipe, recieve_pipe):
    text = recieve_pipe.recv()

    stats = {
        "total_letters": 0,
        "total_digits": 0,
        "total_length": 0,
        "longest_word":  text if text != "close" else "",
        "shortest_word": text if text != "close" else ""
    }

    while text != "close":
        word_length = len(text)

        if word_length > len(stats["longest_word"]):
            stats["longest_word"] = text
        elif word_length < len(stats["shortest_word"]):
            stats["shortest_word"] = text

        for char in text:
            if char.isalpha():
                stats["total_letters"] += 1
            elif char.isdigit():
                stats["total_digits"] += 1

        stats["total_length"] += word_length
        text = recieve_pipe.recv()

    send_pipe.send(stats)

if __name__ == '__main__':
    father()
