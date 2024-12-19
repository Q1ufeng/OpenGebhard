import psutil
import time
import plotly.graph_objects as go
from cpu_mo import cpu_mo
from diskio_mo import diskio_mo
from diskusage_mo import diskusage_mo
from memory_mo import memory_mo


def main():
    a = memory_mo(10)
    for x in a[1]:
        print(x)


if __name__ == "__main__":
    main()
