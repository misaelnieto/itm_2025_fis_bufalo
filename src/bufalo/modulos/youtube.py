import os
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

import click
import imageio_ffmpeg

try:
    from yt_dlp import YoutubeDL
except ImportError:  # pragma: no cover
    # This should not happen if dependencies are installed correctly
    click.echo("ERROR: yt-dlp is not installed.", err=True)
    sys.exit(1)


@click.group()
def youtube() -> None:
    """Comandos para descargar videos de YouTube."""
    pass


@youtube.command()
@click.argument("url")
@click.option(
    "--type",
    "download_type",
    type=click.Choice(["audio", "video"]),
    prompt="¿Quieres descargar solo el audio o el video completo?",
    help="Tipo de descarga: audio o video",
)
@click.option(
    "-o",
    "--output",
    default=str(Path.home() / "Downloads"),
    help="Directorio de salida (default: ~/Downloads)",
)
def download(
    url: str,
    download_type: str,
    output: str,
) -> None:
    """Descarga videos o audio de YouTube desde una URL."""

    # Validar URL
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        click.echo(
            f"Error: La entrada '{url}' no parece ser un enlace válido. "
            "Asegúrate de incluir http:// o https://",
            err=True,
        )
        sys.exit(1)

    valid_domains = {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"}
    if parsed_url.netloc.lower() not in valid_domains:
        click.echo(
            f"Error: El dominio '{parsed_url.netloc}' no es válido. "
            "Solo se permiten enlaces de YouTube.",
            err=True,
        )
        sys.exit(1)

    out_dir = Path(output).expanduser()
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(out_dir, os.W_OK):
            raise PermissionError("Permiso denegado de escritura")
    except Exception as e:
        click.echo(
            f"Error: No se puede acceder al directorio de salida '{output}': {e}",
            err=True,
        )
        sys.exit(1)

    # Get ffmpeg executable from imageio-ffmpeg if not provided
    try:
        ffmpeg_location = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_location = None

    # Validar existencia de ffmpeg
    if not ffmpeg_location and not shutil.which("ffmpeg"):
        click.echo(
            "Error: No se encontró ffmpeg. Es necesario para procesar los videos.",
            err=True,
        )
        sys.exit(1)

    ydl_opts = {
        "outtmpl": str(out_dir / "%(title)s [%(id)s].%(ext)s"),
        "noprogress": False,
        "continuedl": True,
        "ignoreerrors": "only_download",
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 4,
        "restrictfilenames": True,
    }

    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    if download_type == "audio":
        ydl_opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    else:
        ydl_opts.update(
            {
                "format": (
                    "bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                ),
                "merge_output_format": "mp4",
                "postprocessors": [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": "mp4",
                    }
                ],
            }
        )

    try:
        click.echo(f"Iniciando descarga de: {url}")
        with YoutubeDL(ydl_opts) as ydl:
            retcode = ydl.download([url])

        if retcode != 0:
            click.echo(f"Completado con errores (código {retcode}).", err=True)
            sys.exit(retcode)
        else:
            click.echo("Descarga completada exitosamente.")

    except Exception as e:
        click.echo(f"La descarga falló: {e}", err=True)
        sys.exit(2)
