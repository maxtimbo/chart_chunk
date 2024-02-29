import click

from pathlib import Path

from wavdata.wavdata import WavData


@click.command()
@click.argument('audio', type=click.Path(exists=True))
@click.option('--create_copy', is_flag=True)
def cli(audio, create_copy):
    audio = Path(audio)
    if audio.suffix == '.wav':
        wav_info = WavData(audio)
        wav_info.get_riff_data()
        click.echo(f'{"RIFF DATA":^40}')
        for k, v in wav_info.riff_data.items():
            click.echo(f'{k:<20}: {v}')

        click.echo(wav_info.current_position)

        click.echo(f'\n{"DATA META":^40}')
        for k, v in wav_info.data_meta.items():
            click.echo(f'{k:<20}: {v}')

        if wav_info.is_scott:
            click.echo(f'\n{"The file has a scott header":^40}')
            click.echo(f'{"SCOT DATA":^40}')
            for k, v in wav_info.scott_data.items():
                click.echo(f'{k:<20}: {v}')
        else:
            click.echo(f'\n{"The file does not have a scott header":^40}')

    else:
        click.echo('File must be a wav')


if __name__ == '__main__':
    cli()

