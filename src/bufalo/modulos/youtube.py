import click
from pathlib import Path
import sys
import imageio_ffmpeg

try:
    from yt_dlp import YoutubeDL
except ImportError:
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
    "-o", "--output", default=str(Path.home() / "Downloads"), help="Directorio de salida (default: ~/Downloads)"
)
@click.option(
    "--format",
    default="bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    help='Selección de formato (default: "bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best")',
)
@click.option("--rate", help="Límite de velocidad de descarga (ej. 5M, 500K)")
@click.option(
    "--cookies",
    help="Ruta a archivo cookies.txt (formato Netscape) para videos privados",
)
@click.option(
    "--proxy", help="URL del proxy HTTP/HTTPS si es necesario"
)
@click.option(
    "--skip-existing",
    is_flag=True,
    help="Saltar archivos que ya existen en disco",
)
@click.option(
    "--no-mtime",
    is_flag=True,
    help="No usar el encabezado Last-modified para la fecha del archivo",
)
@click.option(
    "--concurrent-fragments",
    type=int,
    default=4,
    help="Número de fragmentos a descargar concurrentemente (default: 4)",
)
@click.option(
    "--ffmpeg-location",
    help="Ruta a binarios ffmpeg/ffprobe (directorio o ruta completa)",
)
def download(
    url: str,
    download_type: str,
    output: str,
    format: str,
    rate: str | None,
    cookies: str | None,
    proxy: str | None,
    skip_existing: bool,
    no_mtime: bool,
    concurrent_fragments: int,
    ffmpeg_location: str | None,
) -> None:
    """Descarga videos o audio de YouTube desde una URL."""
    
    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Get ffmpeg executable from imageio-ffmpeg if not provided
    if not ffmpeg_location:
        try:
            ffmpeg_location = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            # Fallback or let yt-dlp try to find it
            pass

    ydl_opts = {
        "outtmpl": str(out_dir / "%(title)s [%(id)s].%(ext)s"),
        "noprogress": False,
        "continuedl": True,
        "ignoreerrors": "only_download",
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": max(1, concurrent_fragments),
        "restrictfilenames": True,
    }

    if download_type == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        })
    else:
        ydl_opts.update({
            "format": format,
            "merge_output_format": "mp4",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        })

    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    if cookies:
        ydl_opts["cookiefile"] = cookies
    if rate:
        ydl_opts["ratelimit"] = rate
    if proxy:
        ydl_opts["proxy"] = proxy
    if skip_existing:
        ydl_opts["overwrites"] = False
    if no_mtime:
        ydl_opts["updatetime"] = False

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
