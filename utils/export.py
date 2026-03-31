import io
import zipfile


def build_zip(blog: str, social: str, email: str) -> bytes:
    """Package all three content pieces into a ZIP and return raw bytes."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        if blog:
            zf.writestr("blog_post.txt", blog)
        if social:
            zf.writestr("social_thread.txt", social)
        if email:
            zf.writestr("email_newsletter.txt", email)
    buf.seek(0)
    return buf.read()