from typing import Dict

from .types import MessageTemplate

USER_MESSAGES: Dict[str, MessageTemplate] = {
    "USER_NOT_FOUND": {
        "id": "USER_NOT_FOUND",
        "messages": {
            "en": "Invalid credentials. Please check your login details.",
            "uz": "Ushbu ma'lumotlar bo'yicha foydalanuvchi topilmadi.",
            "ru": "Неверные учетные данные. Пожалуйста, проверьте свои данные для входа.",
        },
        "status_code": 400,
    },
    "USER_IS_NOT_ACTIVE": {
        "id": "USER_IS_NOT_ACTIVE",
        "messages": {
            "en": "User is not active.",
            "uz": "Faol foydalanuvchi emas.",
            "ru": "Пользователь неактивен.",
        },
        "status_code": 400,
    },
    "TOKEN_GENERATING_ERROR": {
        "id": "TOKEN_GENERATING_ERROR",
        "messages": {
            "en": "Error happens while generating tokens.",
            "uz": "Token yaratishda xatolik yuz berdi.",
            "ru": "Ошибка возникает при генерации токенов.",
        },
        "status_code": 500,
    },
    "INVALID_TOKEN": {
        "id": "INVALID_TOKEN",
        "messages": {
            "en": "Invalid token",
            "uz": "Token yaroqli emas.",
            "ru": "Недействительный токен",
        },
        "status_code": 500,
    },
    # ── Email ──────────────────────────────────────────────────────────────
    "EMAIL_EXIST_ERROR": {
        "id": "EMAIL_EXIST_ERROR",
        "messages": {
            "en": "An account with this email already exists.",
            "uz": "Bu email allaqachon ro'yxatdan o'tgan.",
            "ru": "Аккаунт с таким email уже существует.",
        },
        "status_code": 400,
    },
    "INVALID_EMAIL_FORMAT": {
        "id": "INVALID_EMAIL_FORMAT",
        "messages": {
            "en": "Invalid email address format.",
            "uz": "Noto'g'ri email formati.",
            "ru": "Неверный формат email адреса.",
        },
        "status_code": 400,
    },
    "INVALID_EMAIL": {
        "id": "INVALID_EMAIL",
        "messages": {
            "en": "The email address does not match.",
            "uz": "Email manzili mos emas.",
            "ru": "Email адрес не совпадает.",
        },
        "status_code": 400,
    },
    # ── Phone (kept for contact-info fields) ──────────────────────────────
    "PHONE_NUMBER_EXIST_ERROR": {
        "id": "PHONE_NUMBER_EXIST_ERROR",
        "messages": {
            "en": "Phone number already exists.",
            "uz": "Bu telefon raqami allaqachon mavjud.",
            "ru": "Этот номер телефона уже существует.",
        },
        "status_code": 400,
    },
    "INVALID_PHONE_NUMBER_FORMAT": {
        "id": "INVALID_PHONE_NUMBER_FORMAT",
        "messages": {
            "en": "Invalid phone number format.",
            "uz": "Noto'g'ri telefon raqami formati.",
            "ru": "Неверный формат номера телефона.",
        },
        "status_code": 400,
    },
    "INVALID_PHONE_NUMBER": {
        "id": "INVALID_PHONE_NUMBER",
        "messages": {
            "en": "Invalid phone number.",
            "uz": "Noto'g'ri telefon raqami.",
            "ru": "Неверный номер телефона.",
        },
        "status_code": 400,
    },
    # ── Registration ──────────────────────────────────────────────────────
    "USER_REGISTERED_SUCCESSFULLY": {
        "id": "USER_REGISTERED_SUCCESSFULLY",
        "messages": {
            "en": "User registered successfully.",
            "uz": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
            "ru": "Пользователь успешно зарегистрирован.",
        },
        "status_code": 201,
    },
    "INVALID_LANGUAGE_TYPE": {
        "id": "INVALID_LANGUAGE_TYPE",
        "messages": {
            "en": "Invalid language type.",
            "uz": "Noto'g'ri til tipi.",
            "ru": "Неверный тип языка.",
        },
        "status_code": 400,
    },
    # ── Verification code ─────────────────────────────────────────────────
    # NOTE: CODE_SENT_SUCCESSFULLY is defined in SHARED_MESSAGES — not here.
    "CODE_VERIFIED_SUCCESSFULLY": {
        "id": "CODE_VERIFIED_SUCCESSFULLY",
        "messages": {
            "en": "Email verified successfully.",
            "uz": "Email muvaffaqiyatli tasdiqlandi.",
            "ru": "Email успешно подтверждён.",
        },
        "status_code": 200,
    },
    "CODE_VERIFICATION_ERROR": {
        "id": "CODE_VERIFICATION_ERROR",
        "messages": {
            "en": "Code verification failed.",
            "uz": "Kod tasdiqlashda xatolik.",
            "ru": "Ошибка подтверждения кода.",
        },
        "status_code": 400,
    },
    "INVALID_VERIFICATION_CODE": {
        "id": "INVALID_VERIFICATION_CODE",
        "messages": {
            "en": "Invalid verification code.",
            "uz": "Noto'g'ri tasdiqlash kodi.",
            "ru": "Неверный код подтверждения.",
        },
        "status_code": 400,
    },
    "VERIFICATION_CODE_EXPIRED": {
        "id": "VERIFICATION_CODE_EXPIRED",
        "messages": {
            "en": "Verification code has expired. Please request a new one.",
            "uz": "Tasdiqlash kodi eskirgan. Yangi kod so'rang.",
            "ru": "Срок действия кода истёк. Запросите новый.",
        },
        "status_code": 400,
    },
    "MAX_VERIFICATION_ATTEMPTS": {
        "id": "MAX_VERIFICATION_ATTEMPTS",
        "messages": {
            "en": "Too many incorrect attempts. Please request a new code.",
            "uz": "Juda ko'p noto'g'ri urinish. Yangi kod so'rang.",
            "ru": "Слишком много неверных попыток. Запросите новый код.",
        },
        "status_code": 429,
    },
    # ── Resend ────────────────────────────────────────────────────────────
    "RESEND_CODE_ERROR": {
        "id": "RESEND_CODE_ERROR",
        "messages": {
            "en": "Failed to resend code.",
            "uz": "Kod qayta yuborilmadi.",
            "ru": "Не удалось повторно отправить код.",
        },
        "status_code": 400,
    },
    "RESEND_CODE_COOLDOWN": {
        "id": "RESEND_CODE_COOLDOWN",
        "messages": {
            "en": "Please wait before requesting another code.",
            "uz": "Iltimos, yangi kod so'rashdan oldin kuting.",
            "ru": "Пожалуйста, подождите перед повторной отправкой кода.",
        },
        "status_code": 429,
    },
    # ── Login ─────────────────────────────────────────────────────────────
    "LOGIN_ERROR": {
        "id": "LOGIN_ERROR",
        "messages": {
            "en": "Login failed.",
            "uz": "Kirish amalga oshmadi.",
            "ru": "Ошибка входа.",
        },
        "status_code": 400,
    },
    "LOGIN_SUCCESS": {
        "id": "LOGIN_SUCCESS",
        "messages": {
            "en": "Login successful.",
            "uz": "Muvaffaqiyatli kirildi.",
            "ru": "Вход выполнен успешно.",
        },
        "status_code": 200,
    },
    # ── Password ─────────────────────────────────────────────────────────
    "SET_PASSWORD_ERROR": {
        "id": "SET_PASSWORD_ERROR",
        "messages": {
            "en": "Failed to set password.",
            "uz": "Parolni o'rnatib bo'lmadi.",
            "ru": "Не удалось установить пароль.",
        },
        "status_code": 400,
    },
    "PASSWORD_SET_SUCCESSFULLY": {
        "id": "PASSWORD_SET_SUCCESSFULLY",
        "messages": {
            "en": "Password set successfully.",
            "uz": "Parol muvaffaqiyatli o'rnatildi.",
            "ru": "Пароль успешно установлен.",
        },
        "status_code": 200,
    },
    "UPDATE_PASSWORD_ERROR": {
        "id": "UPDATE_PASSWORD_ERROR",
        "messages": {
            "en": "Failed to update password.",
            "uz": "Parolni yangilab bo'lmadi.",
            "ru": "Не удалось обновить пароль.",
        },
        "status_code": 400,
    },
    "PASSWORD_UPDATED_SUCCESSFULLY": {
        "id": "PASSWORD_UPDATED_SUCCESSFULLY",
        "messages": {
            "en": "Password updated successfully.",
            "uz": "Parol muvaffaqiyatli yangilandi.",
            "ru": "Пароль успешно обновлён.",
        },
        "status_code": 200,
    },
    "PASSWORD_TOO_SHORT": {
        "id": "PASSWORD_TOO_SHORT",
        "messages": {
            "en": "Password must be at least 6 characters.",
            "uz": "Parol kamida 6 ta belgidan iborat bo'lishi kerak.",
            "ru": "Пароль должен содержать не менее 6 символов.",
        },
        "status_code": 400,
    },
    "PASSWORDS_DO_NOT_MATCH": {
        "id": "PASSWORDS_DO_NOT_MATCH",
        "messages": {
            "en": "Passwords do not match.",
            "uz": "Parollar mos emas.",
            "ru": "Пароли не совпадают.",
        },
        "status_code": 400,
    },
    "INVALID_OLD_PASSWORD": {
        "id": "INVALID_OLD_PASSWORD",
        "messages": {
            "en": "Old password is incorrect.",
            "uz": "Eski parol noto'g'ri.",
            "ru": "Старый пароль неверный.",
        },
        "status_code": 400,
    },
    "INVALID_CREDENTIALS": {
        "id": "INVALID_CREDENTIALS",
        "messages": {
            "en": "Invalid credentials.",
            "uz": "Noto'g'ri ma'lumotlar.",
            "ru": "Неверные учетные данные.",
        },
        "status_code": 400,
    },
    # ── User state ────────────────────────────────────────────────────────
    "USER_DATA_SUCCESS": {
        "id": "USER_DATA_SUCCESS",
        "messages": {
            "en": "User data fetched successfully.",
            "uz": "Foydalanuvchi ma'lumotlari olindi.",
            "ru": "Данные пользователя успешно получены.",
        },
        "status_code": 200,
    },
    "USER_NOT_VERIFIED": {
        "id": "USER_NOT_VERIFIED",
        "messages": {
            "en": "Your email is not verified. Please verify before logging in.",
            "uz": "Emailingiz tasdiqlanmagan. Kirish uchun avval tasdiqlang.",
            "ru": "Ваш email не подтверждён. Подтвердите перед входом.",
        },
        "status_code": 403,
    },
    # ── Email update flow ─────────────────────────────────────────────────
    "UPDATE_EMAIL_ERROR": {
        "id": "UPDATE_EMAIL_ERROR",
        "messages": {
            "en": "Failed to initiate email update.",
            "uz": "Emailni yangilashni boshlash amalga oshmadi.",
            "ru": "Не удалось начать обновление email.",
        },
        "status_code": 400,
    },
    "EMAIL_UPDATE_CODE_SENT": {
        "id": "EMAIL_UPDATE_CODE_SENT",
        "messages": {
            "en": "Verification code sent to your new email address.",
            "uz": "Tasdiqlash kodi yangi email manzilingizga yuborildi.",
            "ru": "Код подтверждения отправлен на новый email адрес.",
        },
        "status_code": 200,
    },
    "VERIFY_UPDATE_EMAIL_ERROR": {
        "id": "VERIFY_UPDATE_EMAIL_ERROR",
        "messages": {
            "en": "Email verification failed.",
            "uz": "Email tasdiqlanmadi.",
            "ru": "Ошибка подтверждения email.",
        },
        "status_code": 400,
    },
    "EMAIL_UPDATED_SUCCESSFULLY": {
        "id": "EMAIL_UPDATED_SUCCESSFULLY",
        "messages": {
            "en": "Email address updated successfully.",
            "uz": "Email manzili muvaffaqiyatli yangilandi.",
            "ru": "Email адрес успешно обновлён.",
        },
        "status_code": 200,
    },
    # ── Profile ───────────────────────────────────────────────────────────
    "PROFILE_UPDATE_ERROR": {
        "id": "PROFILE_UPDATE_ERROR",
        "messages": {
            "en": "Failed to update profile.",
            "uz": "Profilni yangilab bo'lmadi.",
            "ru": "Не удалось обновить профиль.",
        },
        "status_code": 400,
    },
    "PROFILE_UPDATED_SUCCESSFULLY": {
        "id": "PROFILE_UPDATED_SUCCESSFULLY",
        "messages": {
            "en": "Profile updated successfully.",
            "uz": "Profil muvaffaqiyatli yangilandi.",
            "ru": "Профиль успешно обновлён.",
        },
        "status_code": 200,
    },
    # ── Phone update (legacy — kept in case existing clients still use it) ─
    "PHONE_UPDATE_CODE_SENT": {
        "id": "PHONE_UPDATE_CODE_SENT",
        "messages": {
            "en": "Verification code sent to new phone number.",
            "uz": "Tasdiqlash kodi yangi raqamga yuborildi.",
            "ru": "Код подтверждения отправлен на новый номер.",
        },
        "status_code": 200,
    },
    "VERIFY_UPDATE_CODE_ERROR": {
        "id": "VERIFY_UPDATE_CODE_ERROR",
        "messages": {
            "en": "Phone verification failed.",
            "uz": "Telefon tasdiqlanmadi.",
            "ru": "Ошибка подтверждения телефона.",
        },
        "status_code": 400,
    },
    "PHONE_UPDATED_SUCCESSFULLY": {
        "id": "PHONE_UPDATED_SUCCESSFULLY",
        "messages": {
            "en": "Phone number updated successfully.",
            "uz": "Telefon raqami muvaffaqiyatli yangilandi.",
            "ru": "Номер телефона успешно обновлён.",
        },
        "status_code": 200,
    },
}
