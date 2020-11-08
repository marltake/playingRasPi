from . import pattern, neo_pixel


def main():
    generator = pattern.generators[1]
    print(generator)
    neo_pixel.run(generator)


if __name__ == "__main__":
    main()
