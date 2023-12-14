from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

DEFAULT_SINGLETON_INSTANCE_ID = 1


class AbstractSingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Always save as the first and only model
        """
        self.pk = DEFAULT_SINGLETON_INSTANCE_ID
        super().save(*args, **kwargs)


class CommonSettings(AbstractSingletonModel):
    """
    Settings which are common across more than 1 parser
    """

    class OutputTypeChoices(models.TextChoices):
        PDF = ("pdf", _("pdf"))
        PDF_A = ("pdfa", _("pdfa"))
        PDF_A1 = ("pdfa-1", _("pdfa-1"))
        PDF_A2 = ("pdfa-2", _("pdfa-2"))
        PDF_A3 = ("pdfa-3", _("pdfa-3"))

    output_type = models.CharField(
        verbose_name=_("Sets the output PDF type"),
        null=True,
        blank=True,
        max_length=8,
        choices=OutputTypeChoices.choices,
    )


class OcrSettings(AbstractSingletonModel):
    """
    Settings for the Tesseract based OCR parser
    """

    class ModeChoices(models.TextChoices):
        SKIP = ("skip", _("skip"))
        SKIP_NO_ARCHIVE = ("skip_noarchive", _("skip_noarchive"))
        REDO = ("redo", _("redo"))
        FORCE = ("force", _("force"))

    class ArchiveFileChoices(models.TextChoices):
        NEVER = ("never", _("never"))
        WITH_TEXT = ("with_text", _("with_text"))
        ALWAYS = ("always", _("always"))

    class CleanChoices(models.TextChoices):
        CLEAN = ("clean", _("clean"))
        FINAL = ("clean-final", _("clean-final"))
        NONE = ("none", _("none"))

    class ColorConvertChoices(models.TextChoices):
        UNCHANGED = ("LeaveColorUnchanged", _("LeaveColorUnchanged"))
        RGB = ("RGB", _("RGB"))
        INDEPENDENT = ("UseDeviceIndependentColor", _("UseDeviceIndependentColor"))
        GRAY = ("Gray", _("Gray"))
        CMYK = ("CMYK", _("CMYK"))

    pages = models.PositiveIntegerField(
        verbose_name=_("Do OCR from page 1 to this value"),
        null=True,
        blank=True,
    )

    language = models.CharField(
        verbose_name=_("Do OCR using these languages"),
        null=True,
        blank=True,
        max_length=32,
    )

    mode = models.CharField(
        verbose_name=_("Sets the OCR mode"),
        null=True,
        blank=True,
        max_length=8,
        choices=ModeChoices.choices,
    )

    skip_archive_file = models.CharField(
        verbose_name=_("Controls the generation of an archive file"),
        null=True,
        blank=True,
        max_length=16,
        choices=ArchiveFileChoices.choices,
    )

    image_dpi = models.PositiveIntegerField(
        verbose_name=_("Sets image DPI fallback value"),
        null=True,
    )

    # Can't call it clean, that's a model method
    unpaper_clean = models.CharField(
        verbose_name=_("Controls the unpaper cleaning"),
        null=True,
        blank=True,
        max_length=16,
        choices=CleanChoices.choices,
    )

    deskew = models.BooleanField(verbose_name=_("Enables deskew"), null=True)

    rotate_pages = models.BooleanField(
        verbose_name=_("Enables page rotation"),
        null=True,
    )

    rotate_pages_threshold = models.FloatField(
        verbose_name=_("Sets the threshold for rotation of pages"),
        null=True,
        validators=[MinValueValidator(0.0)],
    )

    max_image_pixels = models.FloatField(
        verbose_name=_("Sets the maximum image size for decompression"),
        null=True,
        validators=[MinValueValidator(1_000_000.0)],
    )

    color_conversion_strategy = models.CharField(
        verbose_name=_("Sets the Ghostscript color conversion strategy"),
        blank=True,
        null=True,
        max_length=32,
        choices=ColorConvertChoices.choices,
    )

    user_args = models.JSONField(
        verbose_name=_("Adds additional user arguments for OCRMyPDF"),
        null=True,
    )

    class Meta:
        verbose_name = _("ocr settings")

    def __str__(self) -> str:
        return "OcrSettings"
