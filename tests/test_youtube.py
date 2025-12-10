from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from bufalo.modulos.youtube import youtube


@patch("bufalo.modulos.youtube.YoutubeDL")
@patch("bufalo.modulos.youtube.imageio_ffmpeg")
def test_download_audio(mock_ffmpeg, mock_ydl):
    """Prueba la descarga de solo audio."""
    # Mock ffmpeg path
    mock_ffmpeg.get_ffmpeg_exe.return_value = "/path/to/ffmpeg"

    # Mock YoutubeDL context manager
    mock_instance = MagicMock()
    mock_instance.download.return_value = 0
    mock_ydl.return_value.__enter__.return_value = mock_instance

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "audio"]
    )

    assert result.exit_code == 0
    assert "Iniciando descarga" in result.output

    # Verify YoutubeDL was called with correct options
    call_args = mock_ydl.call_args[0][0]
    assert call_args["format"] == "bestaudio/best"
    assert call_args["ffmpeg_location"] == "/path/to/ffmpeg"
    assert any(pp["key"] == "FFmpegExtractAudio" for pp in call_args["postprocessors"])


@patch("bufalo.modulos.youtube.YoutubeDL")
@patch("bufalo.modulos.youtube.imageio_ffmpeg")
def test_download_video(mock_ffmpeg, mock_ydl):
    """Prueba la descarga de video completo."""
    mock_ffmpeg.get_ffmpeg_exe.return_value = "/path/to/ffmpeg"

    mock_instance = MagicMock()
    mock_instance.download.return_value = 0
    mock_ydl.return_value.__enter__.return_value = mock_instance

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "video"]
    )

    assert result.exit_code == 0

    # Verify YoutubeDL options
    call_args = mock_ydl.call_args[0][0]
    assert call_args["merge_output_format"] == "mp4"
    assert any(
        pp["key"] == "FFmpegVideoConvertor" for pp in call_args["postprocessors"]
    )


def test_invalid_url_scheme():
    runner = CliRunner()
    # "www.youtube.com" without scheme will result in empty scheme in urlparse
    result = runner.invoke(youtube, ["download", "www.youtube.com", "--type", "video"])
    assert result.exit_code == 1
    assert "no parece ser un enlace válido" in result.output


def test_invalid_domain():
    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://google.com", "--type", "video"]
    )
    assert result.exit_code == 1
    assert "no es válido. Solo se permiten enlaces de YouTube" in result.output


@patch("bufalo.modulos.youtube.os.access")
@patch("bufalo.modulos.youtube.Path.mkdir")
def test_output_dir_write_permission_error(mock_mkdir, mock_access):
    # mkdir succeeds
    mock_mkdir.return_value = None
    # os.access returns False (no write permission)
    mock_access.return_value = False

    runner = CliRunner()
    result = runner.invoke(
        youtube,
        [
            "download",
            "https://youtube.com/watch?v=123",
            "--type",
            "video",
            "-o",
            "/root/protected",
        ],
    )
    assert result.exit_code == 1
    assert "No se puede acceder al directorio" in result.output


@patch("bufalo.modulos.youtube.imageio_ffmpeg.get_ffmpeg_exe")
@patch("bufalo.modulos.youtube.shutil.which")
def test_missing_ffmpeg(mock_shutil_which, mock_get_exe):
    # Simulate imageio failure AND no system ffmpeg
    mock_get_exe.side_effect = Exception("Not found")
    mock_shutil_which.return_value = None

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "video"]
    )
    assert result.exit_code == 1
    assert "No se encontró ffmpeg" in result.output


@patch("bufalo.modulos.youtube.imageio_ffmpeg.get_ffmpeg_exe")
@patch("bufalo.modulos.youtube.shutil.which")
@patch("bufalo.modulos.youtube.YoutubeDL")
def test_imageio_fails_but_system_ffmpeg_exists(
    mock_ydl, mock_shutil_which, mock_get_exe
):
    # Simulate imageio failure BUT system ffmpeg exists
    mock_get_exe.side_effect = Exception("No binary")
    mock_shutil_which.return_value = "/usr/bin/ffmpeg"

    mock_instance = MagicMock()
    mock_instance.download.return_value = 0
    mock_ydl.return_value.__enter__.return_value = mock_instance

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "video"]
    )
    assert result.exit_code == 0
    assert "Descarga completada exitosamente" in result.output


@patch("bufalo.modulos.youtube.YoutubeDL")
@patch("bufalo.modulos.youtube.imageio_ffmpeg")
def test_download_nonzero_retcode(mock_ffmpeg, mock_ydl):
    mock_ffmpeg.get_ffmpeg_exe.return_value = "/bin/ffmpeg"

    mock_instance = MagicMock()
    mock_instance.download.return_value = 1  # Non-zero return code
    mock_ydl.return_value.__enter__.return_value = mock_instance

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "video"]
    )
    assert result.exit_code == 1
    assert "Completado con errores" in result.output


@patch("bufalo.modulos.youtube.YoutubeDL")
@patch("bufalo.modulos.youtube.imageio_ffmpeg")
def test_download_exception(mock_ffmpeg, mock_ydl):
    mock_ffmpeg.get_ffmpeg_exe.return_value = "/bin/ffmpeg"
    # Mock exception during download
    mock_ydl.return_value.__enter__.side_effect = Exception("Download error")

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "video"]
    )

    assert result.exit_code == 2
    assert "La descarga falló" in result.output
