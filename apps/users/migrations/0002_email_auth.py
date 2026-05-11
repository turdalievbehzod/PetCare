"""
Migration: switch primary auth identifier from phone_number to email.

Changes:
  User
  - phone_number: NOT NULL unique → NULL unique (optional contact field)
  - email: NULL → NOT NULL (now the primary identifier / USERNAME_FIELD)
  - temp_email: new field for the email-update verification flow
  VerificationCode
  - attempts: new field for brute-force protection
  - expiration_seconds: default 120 → 300 (5 min)
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        # ── User: phone_number becomes optional ─────────────────────────────
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                blank=True, db_index=True, max_length=20, null=True, unique=True
            ),
        ),
        # ── User: email becomes required (NOT NULL) ──────────────────────────
        # Step 1: allow null temporarily so existing rows aren't rejected
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True, db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        # Step 2: fill any NULL emails from phone_number so the NOT NULL
        #         constraint can be added safely on an already-populated table
        migrations.RunSQL(
            sql="""
                UPDATE users
                SET email = CONCAT('phone_', phone_number, '@placeholder.invalid')
                WHERE email IS NULL AND phone_number IS NOT NULL;

                UPDATE users
                SET email = CONCAT('user_', id, '@placeholder.invalid')
                WHERE email IS NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Step 3: make email NOT NULL
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                db_index=True, max_length=255, unique=True
            ),
        ),
        # ── User: add temp_email ─────────────────────────────────────────────
        migrations.AddField(
            model_name="user",
            name="temp_email",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        # ── VerificationCode: brute-force attempt counter ────────────────────
        migrations.AddField(
            model_name="verificationcode",
            name="attempts",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        # ── VerificationCode: extend default expiry to 5 min ─────────────────
        migrations.AlterField(
            model_name="verificationcode",
            name="expiration_seconds",
            field=models.PositiveSmallIntegerField(default=300),
        ),
    ]
