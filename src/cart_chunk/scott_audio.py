import click

from pathlib import Path

from wavdata.wavdata import WavData


@click.group(invoke_without_command=True)
@click.argument('audio', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, audio):
    audio = Path(audio)
    if audio.suffix == '.wav':
        wav = WavData(audio)
        click.echo(f'{"WAVE DATA":^40}')
        for k, v in wav.wave_data.items():
            click.echo(f'{k:<20}: {v}')

        wav.get_riff_data()

        click.echo(f'{"RIFF DATA":^40}')
        for k, v in wav.riff_data.items():
            click.echo(f'{k:<20}: {v}')

        click.echo(f'{"FMT DATA":^40}')
        for k, v in wav.fmt_data.items():
            click.echo(f'{k:<20}: {v}')

        wav.get_scott_data()
        wav.get_data_size()
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
    wav.write_copy(artist, title)
    #wav.create_copy(new_audio, artist, title)


if __name__ == '__main__':
    cli()

