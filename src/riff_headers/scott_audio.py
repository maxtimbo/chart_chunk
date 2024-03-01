import click

from pathlib import Path

from wavdata.wavdata import WavData


@click.group()
@click.argument('audio', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, audio):
    audio = Path(audio)
    if audio.suffix == '.wav':
        wav = WavData(audio)
        wav.get_riff_data()
        click.echo(f'{"RIFF DATA":^40}')
        for k, v in wav.riff_data.items():
            click.echo(f'{k:<20}: {v}')


        click.echo(f'\n{"DATA META":^40}')
        for k, v in wav.data_meta.items():
            click.echo(f'{k:<20}: {v}')

        if wav.is_scott:
            click.echo(f'\n{"The file has a scott header":^40}')
            click.echo(f'{"SCOT DATA":^40}')
            for k, v in wav.scott_data.items():
                click.echo(f'{k:<20}: {v}')

        else:
            click.echo(f'\n{"The file does not have a scott header":^40}')

        click.echo(f'End of riff/fmt chunk: {wav.riff_fmt_end}')
        if wav.is_scott:
            click.echo(f'Scott begin byte position: {wav.scott_begin}')
            click.echo(f'Scott end byte position: {wav.scott_end}')
            click.echo(f'Scott end fillout byte position: {wav.scott_end_fillout}')

        click.echo(f'Data byte position: {wav.data_position}')
        ctx.ensure_object(dict)
        ctx.obj['wav'] = wav

    else:
        click.echo('File must be a wav')

@cli.command()
@click.argument('new_audio')
@click.argument('artist')
@click.argument('title')
@click.pass_context
def create_copy(ctx, new_audio, artist, title):
    wav = ctx.obj.get('wav')
    #wav.create_copy(new_audio, artist, title)


if __name__ == '__main__':
    cli()

