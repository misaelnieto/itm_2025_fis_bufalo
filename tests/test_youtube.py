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


@patch("bufalo.modulos.youtube.YoutubeDL")
def test_download_failure(mock_ydl):
    """Prueba el manejo de errores en la descarga."""
    # Mock exception
    mock_ydl.return_value.__enter__.side_effect = Exception("Download error")

    runner = CliRunner()
    result = runner.invoke(
        youtube, ["download", "https://youtube.com/watch?v=123", "--type", "video"]
    )

    assert result.exit_code == 2
    assert "La descarga falló" in result.output
