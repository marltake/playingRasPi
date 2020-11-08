import click
from . import pattern, neo_pixel, switch_control

@click.command()
@click.option("-p", "--pattern-index", type=int)
def main(pattern_index):
    if pattern_index is None:
        switch_control.run()
        return
    generator = pattern.get_generator(pattern_index)
    print(generator)
    neo_pixel.run(generator)


if __name__ == "__main__":
    main()
