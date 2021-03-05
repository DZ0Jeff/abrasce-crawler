import timeit
from time import gmtime
from time import strftime


def arrendondar(numero):
    print("%.2f" % round(numero, 2))


def tempo_estimado(start):
    stop = timeit.default_timer()
    execution_time = stop - start

    print("Executando em: ", end="")
    time_formated_to_seconds = execution_time
    print(strftime("%H:%M:%S", gmtime(time_formated_to_seconds)))

def main():
    for i in range(1000000):
        print(i)


if __name__ == "__main__":
    start = timeit.default_timer()

    try:
        main()

        tempo_estimado(start)

    except KeyboardInterrupt:
        tempo_estimado(start)
