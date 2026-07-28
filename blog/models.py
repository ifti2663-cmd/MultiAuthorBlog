from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS = (
        ("Draft", "Draft"),
        ("Published", "Published"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    content = models.TextField()

    featured_image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Draft"
    )

    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.title)

            slug = base_slug

            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_like"
            )
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"