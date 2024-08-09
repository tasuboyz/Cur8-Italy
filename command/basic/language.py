class Language:
    def __init__(self):
        pass

    def back(self, language_code):
        eng = "Back 🔙"
        lang_text = {
            'it': "Indietro 🔙",
            'en': eng,
            'hi': "पीछे 🔙",
            'es': "Volver 🔙",
            'fr': "Retour 🔙",
            'de': "Zurück 🔙",
            'ru': "Назад 🔙",
            'uk': "Назад 🔙",
            'zh': "返回 🔙",
            'ar': "العودة 🔙"
        }
        return lang_text.get(language_code, eng)
  
    def cancel(self, language_code):
        eng = "Cancel ❌"
        lang_text = {
            'it': "Annulla ❌",
            'en': eng,
            'hi': "रद्द करें ❌",
            'es': "Cancelar ❌",
            'fr': "Annuler ❌",
            'de': "Abbrechen ❌",
            'ru': "Отмена ❌",
            'uk': "Відмінити ❌",
            'zh': "取消 ❌",
            'ar': "إلغاء ❌"
        }
        return lang_text.get(language_code, eng)
    
    def send_image(self, language_code):
        eng = "Send me Image 🌉 or gif 🎞:"
        lang_text = {
            'it': "Inviami un'immagine 🌉 o gif 🎞:",
            'en': eng,
            'hi': "मुझे एक छवि या gif भेजें 🌉🎞:",
            'es': "Envíame una imagen 🌉 o gif 🎞:",
            'fr': "Envoie-moi une image 🌉 ou un gif 🎞:",
            'de': "Sende mir ein Bild 🌉 oder ein gif 🎞:",
            'ru': "Отправь мне изображение 🌉 или gif 🎞:",
            'uk': "Надішли мені зображення 🌉 або gif 🎞:",
            'zh': "发送图片 🌉 或 gif 🎞：",
            'ar': "أرسل لي صورة 🌉 أو gif 🎞:"
        }
        return lang_text.get(language_code, eng)

    def waiting(self, language_code):
        eng = "Waiting..."
        lang_text = {
            'it': "In attesa...",
            'en': eng,
            'hi': "प्रतीक्षा कर रहा हूँ...",
            'es': "Esperando...",
            'fr': "En attente...",
            'de': "Warten...",
            'ru': "Ожидание...",
            'uk': "Очікування...",
            'zh': "等待中...",
            'ar': "في انتظار..."
        }
        return lang_text.get(language_code, eng)

    def error(self, language_code):
        eng = "Ops... an error has occurred 😔 contact owner or try again!"
        lang_text = {
            'it': "Ops... si è verificato un errore 😔 contatta il proprietario o riprova!",
            'en': eng,
            'hi': "ओह... कुछ गड़बड़ हो गई है 😔 मालिक से संपर्क करें या पुनः प्रयास करें!",
            'es': "Ops... ha ocurrido un error 😔 contacta al propietario o inténtalo de nuevo.",
            'fr': "Ops... une erreur s'est produite 😔 contactez le propriétaire ou réessayez !",
            'de': "Oops... ein Fehler ist aufgetreten 😔 kontaktiere den Besitzer oder versuche es erneut!",
            'ru': "Упс... произошла ошибка 😔 свяжитесь с владельцем или попробуйте снова!",
            'uk': "Ой... сталася помилка 😔 зверніться до власника або спробуйте ще раз!",
            'zh': "糟糕... 发生了错误 😔 联系所有者或重试!",
            'ar': "عذرًا... حدث خطأ 😔 اتصل بالمالك أو حاول مرة أخرى!"
        }
        return lang_text.get(language_code, eng)
    
    def file_not_valid(self, language_code):
        eng = "The image file is not valid 🚫"
        lang_text = {
            'it': "Il file dell'immagine non è valido 🚫",
            'en': eng,
            'hi': "चित्र फ़ाइल मान्य नहीं है 🚫",
            'es': "El archivo de imagen no es válido 🚫",
            'fr': "Le fichier image n'est pas valide 🚫",
            'de': "Die Bilddatei ist nicht gültig 🚫",
            'ru': "Файл изображения недопустим 🚫",
            'uk': "Файл зображення недійсний 🚫",
            'zh': "图像文件无效 🚫",
            'ar': "ملف الصورة غير صالح 🚫"
        }
        return lang_text.get(language_code, eng)

    def open_link(self, language_code):
        eng = "Open Link"
        lang_text = {
            'it': "Apri il link",
            'en': eng,
            'hi': "लिंक खोलें",
            'es': "Abrir enlace",
            'fr': "Ouvrir le lien",
            'de': "Link öffnen",
            'ru': "Открыть ссылку",
            'uk': "Відкрити посилання",
            'zh': "打开链接",
            'ar': "افتح الرابط"
        }
        return lang_text.get(language_code, eng)

    def confirm(self, language_code, qr):
        caption_status = '✅' if qr else '⚠️'
        eng = f"Confirm {caption_status}"
        lang_text = {
            'it': f"Conferma {caption_status}",
            'en': eng,
            'hi': f"पुष्टि {caption_status}",
            'es': f"Confirmar {caption_status}",
            'fr': f"Confirmer {caption_status}",
            'de': f"Bestätigen {caption_status}",
            'ru': f"Подтвердить {caption_status}",
            'uk': f"Підтвердити {caption_status}",
            'zh': f"确认 {caption_status}",
            'ar': f"تأكيد {caption_status}"
        }

    def operation_deleted(self, language_code):
        eng = "operation deleted 🗑"
        lang_text = {
            'it': "operazione eliminata 🗑",
            'en': eng,
            'hi': "कार्रवाई हटा दी गई 🗑",
            'es': "operación eliminada 🗑",
            'fr': "opération supprimée 🗑",
            'de': "Operation gelöscht 🗑",
            'ru': "операция удалена 🗑",
            'uk': "операцію видалено 🗑",
            'zh': "操作已删除 🗑",
            'ar': "تم حذف العملية 🗑"
        }
        return lang_text.get(language_code, eng)
    
    def not_member_channel(self, language_code):
        channel_link = '<a href="https://t.me/tasu_Channel">👇</a>'
        eng = f"Join the channel to take advantage of the function! {channel_link}"
        lang_text = {
            'it': f"Entra nel canale per usufruire della funzione! {channel_link}",
            'en': eng,
            'hi': f"कार्रवाई का लाभ उठाने के लिए चैनल में शामिल हों! {channel_link}",
            'es': f"¡Entra al canal para utilizar esta función! {channel_link}",
            'fr': f"Inscrivez-vous sur le canal pour bénéficier de la fonctionnalité! {channel_link}",
            'de': f"Tritt dem Kanal bei, um die Funktion zu nutzen! {channel_link}",
            'ru': f"Вступите в канал, чтобы воспользоваться функцией! {channel_link}",
            'uk': f"Приєднуйтесь до каналу, щоб скористатися функцією! {channel_link}",
            'zh': f"加入频道以利用此功能！{channel_link}",
            'ar': f"انضم إلى القناة للاستفادة من الوظيفة! {channel_link}"
        }
        return lang_text.get(language_code, eng)

    def language_setting(self, language_code):
        eng = "Language setting 🇬🇧"
        lang_text = {
            'it': "Impostazioni Lingua 🇮🇹",
            'en': eng,
            'hi': "भाषा सेटिंग 🇮🇳",
            'es': "Configuración de Idioma 🇪🇸",
            'fr': "Paramètres de Langue 🇫🇷",
            'de': "Spracheinstellungen 🇩🇪",
            'ru': "Настройки Языка 🇷🇺",
            'uk': "Налаштування Мови 🇺🇦",
            'zh': "语言设置 🇨🇳",
            'ar': "إعداد اللغة 🇸🇦"
        }
        return lang_text.get(language_code, eng)
    
    def choose_language(self, language_code):
        lang_text = {
            'it': "Scegli la lingua 🇮🇹",
            'en': "Choose language 🇺🇸",
            'hi': "भाषा चुनें 🇮🇳",
            'es': "Elige el idioma 🇪🇸",
            'fr': "Choisissez la langue 🇫🇷",
            'de': "Wähle die Sprache 🇩🇪",
            'ru': "Выберите язык 🇷🇺",
            'uk': "Оберіть мову 🇺🇦",
            'zh': "选择语言 🇨🇳",
            'ar': "اختر اللغة 🇸🇦"
        }
        return lang_text.get(language_code, "Choose language 🌐")

    def language_setted(self, language_code):
        eng = f"Language setted 🇬🇧"
        if language_code == 'it':
            message = f"Lingua impostata 🇮🇹"
        elif language_code == 'en':
            message = eng
        elif language_code == 'hi':
            message = f"भाषा सेट की गई 🇮🇳"
        elif language_code == 'es':
            message = f"Idioma establecido 🇪🇸"
        elif language_code == 'fr':
            message = f"Langue définie 🇫🇷"
        elif language_code == 'de':
            message = f"Sprache festgelegt 🇩🇪"
        elif language_code == 'ru':
            message = f"Установлен язык 🇷🇺"
        elif language_code == 'uk':
            message = f"Мова встановлена 🇺🇦"
        elif language_code == 'zh':
            message = f"语言已设置 🇨🇳"
        elif language_code == 'ar':
            message = f"تم تعيين اللغة 🇸🇦"
        else:
            message = eng
        return message
    
    def wait_operation(self, language_code):
        eng = "Please wait for the operation to complete ⏳"
        lang_text = {
            'it': "Attendi il completamento dell'operazione ⏳",
            'en': eng,
            'hi': "कृपया कार्रवाई पूर्ण होने की प्रतीक्षा करें ⏳",
            'es': "Espere a que la operación se complete ⏳",
            'fr': "Veuillez patienter pendant que l'opération se termine ⏳",
            'de': "Bitte warten Sie, bis die Operation abgeschlossen ist ⏳",
            'ru': "Пожалуйста, подождите завершения операции ⏳",
            'uk': "Будь ласка, зачекайте завершення операції ⏳",
            'zh': "请等待操作完成 ⏳",
            'ar': "يرجى الانتظار حتى اكتمال العملية ⏳"
        }
        return lang_text.get(language_code, eng)
    
    def buy_premium_pack(self, language_code):
        eng = "Buy the Premium Pack 🛒💎"
        lang_text = {
            'it': "Acquista il Pacchetto Premium 🛒💎",
            'en': eng,
            'hi': "प्रीमियम पैक खरीदें 🛒💎",
            'es': "Compra el Paquete Premium 🛒💎",
            'fr': "Acheter le Pack Premium 🛒💎",
            'de': "Kaufen Sie das Premium-Paket 🛒💎",
            'ru': "Купить премиум-пакет 🛒💎",
            'uk': "Купити преміум-пакет 🛒💎",
            'zh': "购买高级套餐 🛒💎",
            'ar': "شراء حزمة البريميوم 🛒💎"
        }
        return lang_text.get(language_code, eng)

    def error_occurred(self, language_code):
        eng_message = "Oops... an error occurred, please try again or contact @tasuboyz immediately to show them the problem."
        lang_text = {
            'it': "ops... si è verificato un errore, riprova o contatta subito @tasuboyz per mostrargli il problema.",
            'hi': "उफ़... एक त्रुटि हुई है, कृपया पुनः प्रयास करें या समस्या दिखाने के लिए तुरंत @tasuboyz से संपर्क करें।",
            'es': "ups... ocurrió un error, intenta nuevamente o contacta a @tasuboyz inmediatamente para mostrarle el problema.",
            'fr': "oups... une erreur s'est produite, veuillez réessayer ou contacter immédiatement @tasuboyz pour lui montrer le problème.",
            'de': "ups... ein Fehler ist aufgetreten, bitte versuche es erneut oder kontaktiere sofort @tasuboyz, um ihnen das Problem zu zeigen.",
            'ru': "упс... произошла ошибка, пожалуйста, попробуйте снова или немедленно свяжитесь с @tasuboyz, чтобы показать им проблему.",
            'uk': "упс... сталася помилка, будь ласка, спробуйте ще раз або негайно зв'яжіться з @tasuboyz, щоб показати їм проблему.",
            'zh': "哎呀... 出现错误，请重试或立即联系 @tasuboyz 以向他们展示问题。",
            'ar': "عذرًا... حدث خطأ، يرجى المحاولة مرة أخرى أو الاتصال بـ @tasuboyz فورًا لإظهار المشكلة."
        }
        return lang_text.get(language_code, eng_message)

    def click_filter_community(self, language_code):
        example_text = "<code>@cur8_steemBot community: italy</code>"
        eng_message = f"Click filter community: {example_text}"
        lang_text = {
            'it': f"Clicca per filtrare la comunità: {example_text}",
            'hi': f"फिल्टर समुदाय पर क्लिक करें: {example_text}",
            'es': f"Haz clic para filtrar la comunidad: {example_text}",
            'fr': f"Cliquez pour filtrer la communauté: {example_text}",
            'de': f"Klicken Sie, um die Gemeinschaft zu filtern: {example_text}",
            'ru': f"Нажмите, чтобы отфильтровать сообщество: {example_text}",
            'uk': f"Натисніть, щоб відфільтрувати спільноту: {example_text}",
            'zh': f"点击过滤社区: {example_text}",
            'ar': f"انقر لتصفية المجتمع: {example_text}",
            'en': eng_message  # English
        }
        
        return lang_text.get(language_code, eng_message)
    
    def welcome_message(self, first_name, language_code):
        eng_message = (f"Welcome {first_name}\n"
                    "Please log in with your Steem account and enter your posting key. Once logged in, you can send me images to convert them into URLs to insert into your posts. "
                    "Select the community before posting! 📸📝")
        lang_text = {
            'it': (f"Benvenuto {first_name}\n"
                "Effettua l'accesso con il tuo account di Steem e inserisci la tua posting key. Una volta effettuato l'accesso, potrai inviarmi immagini per convertirle in URL da inserire nei tuoi post. "
                "Seleziona prima la community prima di pubblicare un post! 📸📝"),
            'hi': (f"स्वागत है {first_name}\n"
                "कृपया अपने Steem खाते से लॉग इन करें और अपनी पोस्टिंग कुंजी दर्ज करें। लॉग इन करने के बाद, आप मुझे छवियाँ भेज सकते हैं ताकि उन्हें URL में बदल सकें और अपने पोस्ट में डाल सकें। "
                "पोस्ट करने से पहले समुदाय का चयन करें! 📸📝"),
            'es': (f"Bienvenido {first_name}\n"
                "Inicia sesión con tu cuenta de Steem e ingresa tu clave de publicación. Una vez que hayas iniciado sesión, puedes enviarme imágenes para convertirlas en URLs para insertarlas en tus publicaciones. "
                "¡Selecciona la comunidad antes de publicar! 📸📝"),
            'fr': (f"Bienvenue {first_name}\n"
                "Connectez-vous avec votre compte Steem et entrez votre clé de publication. Une fois connecté, vous pouvez m'envoyer des images pour les convertir en URL à insérer dans vos publications. "
                "Sélectionnez d'abord la communauté avant de publier un post! 📸📝"),
            'de': (f"Willkommen {first_name}\n"
                "Melden Sie sich mit Ihrem Steem-Konto an und geben Sie Ihren Posting-Schlüssel ein. Nach der Anmeldung können Sie mir Bilder senden, um sie in URLs zu konvertieren, die Sie in Ihre Posts einfügen können. "
                "Wählen Sie zuerst die Community aus, bevor Sie einen Beitrag veröffentlichen! 📸📝"),
            'ru': (f"Добро пожаловать, {first_name}\n"
                "Пожалуйста, войдите в свою учетную запись Steem и введите свой ключ для публикации. После входа вы можете отправлять мне изображения для их преобразования в URL-адреса для вставки в ваши посты. "
                "Выберите сообщество перед публикацией! 📸📝"),
            'uk': (f"Ласкаво просимо, {first_name}\n"
                "Будь ласка, увійдіть у свій обліковий запис Steem і введіть свій ключ для публікації. Після входу ви можете надсилати мені зображення для перетворення їх у URL-адреси, щоб вставити їх у свої пости. "
                "Виберіть спільноту перед публікацією! 📸📝"),
            'zh': (f"欢迎{first_name}\n"
                "请使用您的Steem帐户登录并输入您的发布密钥。 登录后，您可以发送图片给我，以将其转换为URL以插入到您的帖子中。 "
                "发布帖子前请选择社区！ 📸📝"),
            'ar': (f"مرحبًا {first_name}\n"
                "يرجى تسجيل الدخول باستخدام حساب Steem الخاص بك وإدخال مفتاح النشر الخاص بك. بمجرد تسجيل الدخول، يمكنك إرسال الصور إلي لتحويلها إلى روابط لإدراجها في منشوراتك. "
                "حدد المجتمع قبل النشر! 📸📝")
        }
        return lang_text.get(language_code, eng_message)

    def set_account_password(self, language_code):
        eng_message = "Set your account and password"

        lang_text = {
            'it': "Imposta il tuo account e la tua password",
            'hi': "अपना खाता और पासवर्ड सेट करें",
            'es': "Configura tu cuenta y contraseña",
            'fr': "Définissez votre compte et votre mot de passe",
            'de': "Richten Sie Ihr Konto und Ihr Passwort ein",
            'ru': "Установите свой аккаунт и пароль",
            'uk': "Встановіть свій обліковий запис і пароль",
            'zh': "设置您的帐户和密码",
            'ar': "قم بتعيين حسابك وكلمة المرور الخاصة بك"
        }
        
        return lang_text.get(language_code, eng_message)

    def choose_community(self, language_code):
        example_text = "<code>@cur8_steemBot community: italy</code>"
        eng_message = f"Choose your community 👇 {example_text}"
        lang_text = {
            'it': f"Scegli la tua comunità 👇 {example_text}",
            'hi': f"अपना समुदाय चुनें 👇 {example_text}",
            'es': f"Elige tu comunidad 👇 {example_text}",
            'fr': f"Choisissez votre communauté 👇 {example_text}",
            'de': f"Wählen Sie Ihre Gemeinschaft 👇 {example_text}",
            'ru': f"Выберите ваше сообщество 👇 {example_text}",
            'uk': f"Виберіть свою спільноту 👇 {example_text}",
            'zh': f"选择你的社区 👇 {example_text}",
            'ar': f"اختر مجتمعك 👇 {example_text}",
            'en': eng_message  # English
        }     
        return lang_text.get(language_code, eng_message)
    
    def wrong_password(self, language_code):
        eng_message = "Wrong password 🚫"

        lang_text = {
            'it': "Password errata 🚫",
            'hi': "गलत पासवर्ड 🚫",
            'es': "Contraseña incorrecta 🚫",
            'fr': "Mot de passe incorrect 🚫",
            'de': "Falsches Passwort 🚫",
            'ru': "Неверный пароль 🚫",
            'uk': "Неправильний пароль 🚫",
            'zh': "密码错误 🚫",
            'ar': "كلمة المرور خاطئة 🚫"
        }
        
        return lang_text.get(language_code, eng_message)

    def username_not_exist(self, language_code):
        eng_message = "Username does not exist 🚫"

        lang_text = {
            'it': "Username non esiste 🚫",
            'hi': "उपयोगकर्ता नाम मौजूद नहीं है 🚫",
            'es': "El nombre de usuario no existe 🚫",
            'fr': "Le nom d'utilisateur n'existe pas 🚫",
            'de': "Benutzername existiert nicht 🚫",
            'ru': "Имя пользователя не существует 🚫",
            'uk': "Ім'я користувача не існує 🚫",
            'zh': "用户名不存在 🚫",
            'ar': "اسم المستخدم غير موجود 🚫"
        }
        
        return lang_text.get(language_code, eng_message)

    def login_successful(self, language_code):
        eng_message = "Login successful ✅"

        lang_text = {
            'it': "Accesso riuscito ✅",
            'hi': "लॉगिन सफल ✅",
            'es': "Inicio de sesión exitoso ✅",
            'fr': "Connexion réussie ✅",
            'de': "Anmeldung erfolgreich ✅",
            'ru': "Вход выполнен успешно ✅",
            'uk': "Успішний вхід ✅",
            'zh': "登录成功 ✅",
            'ar': "تسجيل الدخول ناجح ✅"
        }
        
        return lang_text.get(language_code, eng_message)

    def login_for_save_document(self, language_code):
        eng_message = "Login to save document!"

        lang_text = {
            'it': "Accedi per salvare il documento!",
            'hi': "दस्तावेज़ सहेजने के लिए लॉगिन करें!",
            'es': "Inicia sesión para guardar el documento!",
            'fr': "Connectez-vous pour enregistrer le document!",
            'de': "Melden Sie sich an, um das Dokument zu speichern!",
            'ru': "Войдите, чтобы сохранить документ!",
            'uk': "Увійдіть, щоб зберегти документ!",
            'zh': "登录以保存文档！",
            'ar': "قم بتسجيل الدخول لحفظ المستند!"
        }
        
        return lang_text.get(language_code, eng_message)
    
    def search_community(self, language_code):
        lang_text = {
            'it': "Cerca comunità 👥",
            'hi': "समुदाय खोजें 👥",
            'es': "Buscar comunidad 👥",
            'fr': "Rechercher une communauté 👥",
            'de': "Community suchen 👥",
            'ru': "Поиск сообщества 👥",
            'uk': "Шукати спільноту 👥",
            'zh': "搜索社区 👥",
            'ar': "البحث عن المجتمع 👥",
            'en': "Search community 👥"  # English
        }
        
        return lang_text.get(language_code, "Search community 👥")
    
    def login_text(self, language_code):
        lang_text = {
            'it': "Accedi 👤",
            'hi': "लॉगिन करें 👤",
            'es': "Iniciar sesión 👤",
            'fr': "Connexion 👤",
            'de': "Anmelden 👤",
            'ru': "Войти 👤",
            'uk': "Увійти 👤",
            'zh': "登录 👤",
            'ar': "تسجيل الدخول 👤",
            'en': "Login 👤"  # English
        }
        
        return lang_text.get(language_code, "Login 👤")

    def change_account(self, language_code):
        lang_text = {
            'it': "Cambia Account 🔄",
            'hi': "खाता बदलें 🔄",
            'es': "Cambiar Cuenta 🔄",
            'fr': "Changer de Compte 🔄",
            'de': "Konto wechseln 🔄",
            'ru': "Сменить Аккаунт 🔄",
            'uk': "Змінити Обліковий Запис 🔄",
            'zh': "更换账户 🔄",
            'ar': "تغيير الحساب 🔄",
            'en': "Change Account 🔄"  # English
        }
        
        return lang_text.get(language_code, "Change Account 🔄")
    
    def send_post(self, language_code):
        lang_text = {
            'it': "Invia Post 📮",
            'hi': "पोस्ट भेजें 📮",
            'es': "Enviar Publicación 📮",
            'fr': "Envoyer le Post 📮",
            'de': "Beitrag Senden 📮",
            'ru': "Отправить Пост 📮",
            'uk': "Надіслати Пост 📮",
            'zh': "发送帖子 📮",
            'ar': "إرسال المنشور 📮",
            'en': "Send Post 📮"  # English
        }
        
        return lang_text.get(language_code, "Send Post 📮")
    
    def view_community_post(self, language_code):
        lang_text = {
            'it': "Visualizza post della comunità 👀",
            'hi': "समुदाय की पोस्ट देखें 👀",
            'es': "Ver publicación de la comunidad 👀",
            'fr': "Voir le post de la communauté 👀",
            'de': "Gemeinschaftsbeitrag anzeigen 👀",
            'ru': "Просмотреть пост сообщества 👀",
            'uk': "Переглянути пост спільноти 👀",
            'zh': "查看社区帖子 👀",
            'ar': "عرض منشور المجتمع 👀",
            'en': "View community post 👀"  # English
        }
        
        return lang_text.get(language_code, "View community post 👀")

    def public_post_on_community(self, language_code):
        lang_text = {
            'it': "Pubblica post in questa comunità ⬇️",
            'hi': "इस समुदाय पर सार्वजनिक पोस्ट ⬇️",
            'es': "Publicar post en esta comunidad ⬇️",
            'fr': "Publier un post sur cette communauté ⬇️",
            'de': "Beitrag in dieser Gemeinschaft veröffentlichen ⬇️",
            'ru': "Опубликовать пост в этом сообществе ⬇️",
            'uk': "Опублікувати пост у цій спільноті ⬇️",
            'zh': "在此社区发布帖子 ⬇️",
            'ar': "نشر منشور في هذا المجتمع ⬇️",
            'en': "Public Post on this community ⬇️"  # English
        }
        
        return lang_text.get(language_code, "Public Post on this community ⬇️")

    def click_to_send_post(self, language_code):
        lang_text = {
            'it': "Clicca per inviare il post 👇",
            'hi': "पोस्ट भेजने के लिए क्लिक करें 👇",
            'es': "Haz clic para enviar el post 👇",
            'fr': "Cliquez pour envoyer le post 👇",
            'de': "Klicken Sie, um den Beitrag zu senden 👇",
            'ru': "Нажмите, чтобы отправить пост 👇",
            'uk': "Натисніть, щоб надіслати пост 👇",
            'zh': "点击发送帖子 👇",
            'ar': "انقر لإرسال المنشور 👇",
            'en': "Click to Send post 👇"  # English
        }
        
        return lang_text.get(language_code, "Click to Send post 👇")

    def setting(self, language_code):
        lang_text = {
            'it': "Impostazioni ⚙️",
            'hi': "सेटिंग ⚙️",
            'es': "Configuración ⚙️",
            'fr': "Paramètres ⚙️",
            'de': "Einstellungen ⚙️",
            'ru': "Настройки ⚙️",
            'uk': "Налаштування ⚙️",
            'zh': "设置 ⚙️",
            'ar': "الإعدادات ⚙️",
            'en': "Setting ⚙️"  # English
        }
        
        return lang_text.get(language_code, "Setting ⚙️")
    
    def create_account(self, language_code):
        lang_text = {
            'it': "Crea account 🆕",
            'hi': "खाता बनाएं 🆕",
            'es': "Crear cuenta 🆕",
            'fr': "Créer un compte 🆕",
            'de': "Konto erstellen 🆕",
            'ru': "Создать аккаунт 🆕",
            'uk': "Створити акаунт 🆕",
            'zh': "创建账户 🆕",
            'ar': "إنشاء حساب 🆕",
            'en': "Create account 🆕"  # English
        }
        
        return lang_text.get(language_code, "Create account 🆕")
    
    def send_me_username(self, language_code):
        lang_text = {
            'it': "Inviami nome utente:",
            'hi': "मुझे उपयोगकर्ता नाम भेजें:",
            'es': "Envíame el nombre de usuario:",
            'fr': "Envoyez-moi le nom d'utilisateur :",
            'de': "Senden Sie mir den Benutzernamen:",
            'ru': "Отправьте мне имя пользователя:",
            'uk': "Надішліть мені ім'я користувача:",
            'zh': "发送用户名给我：",
            'ar': "أرسل لي اسم المستخدم:",
            'en': "Send me username:"  # English
        }
        
        return lang_text.get(language_code, "Send me username:")

    def choose_option(self, language_code):
        lang_text = {
            'it': "scegli l'opzione:",
            'hi': "विकल्प चुनें:",
            'es': "elige la opción:",
            'fr': "choisissez l'option:",
            'de': "wählen Sie die Option:",
            'ru': "выберите опцию:",
            'uk': "виберіть опцію:",
            'zh': "选择选项：",
            'ar': "اختر الخيار:",
            'en': "choose the option:"  # English
        }     
        return lang_text.get(language_code, "choose the option:")
    
    def wait_for_account(self, language_code):
        lang_text = {
            'it': "⏳ Attendi entro 24H ti verrà restituito il nuovo account con le chiavi, ricorda di tenere al sicuro queste chiavi e non perderle! 🔑",
            'hi': "⏳ 24 घंटे के भीतर आपको नई कुंजियों के साथ नया खाता मिल जाएगा, इन कुंजियों को सुरक्षित रखना याद रखें और इन्हें खोना नहीं! 🔑",
            'es': "⏳ Espera dentro de las 24 horas para recibir la nueva cuenta con las claves, recuerda mantener estas claves seguras y no perderlas! 🔑",
            'fr': "⏳ Attendez sous 24H pour recevoir le nouveau compte avec les clés, n'oubliez pas de garder ces clés en sécurité et de ne pas les perdre! 🔑",
            'de': "⏳ Warten Sie innerhalb von 24 Stunden, um das neue Konto mit den Schlüsseln zu erhalten. Denken Sie daran, diese Schlüssel sicher aufzubewahren und nicht zu verlieren! 🔑",
            'ru': "⏳ Подождите в течение 24 часов, чтобы получить новую учетную запись с ключами, не забудьте сохранить эти ключи в безопасности и не потерять их! 🔑",
            'uk': "⏳ Очікуйте протягом 24 годин на отримання нового облікового запису з ключами, не забудьте зберігати ці ключі в безпеці і не втрачати їх! 🔑",
            'zh': "⏳ 请在24小时内等待，您将收到带有密钥的新账户，记住要保管好这些密钥，不要丢失! 🔑",
            'ar': "⏳ انتظر في غضون 24 ساعة وستحصل على الحساب الجديد مع المفاتيح، تذكر أن تحتفظ بهذه المفاتيح في أمان ولا تفقدها! 🔑",
            'en': "⏳ Wait within 24 hours to receive the new account with keys, remember to keep these keys safe and not lose them! 🔑"  # English
        }

        return lang_text.get(language_code, "⏳ Wait within 24 hours to receive the new account with keys, remember to keep these keys safe and not lose them! 🔑")
    
    def steemit_query_copilot(self, language_code):
        base_url = "https://www.bing.com/search?form=NTPCHT&showconv=1&sendquery=1&q="
        queries = {
            'it': "che+cos'%C3%A8+steemit+%3F",
            'en': "what+is+steemit+%3F",
            'hi': "Steemit+%E0%A4%95%E0%A5%8D%E0%A4%AF%E0%A4%BE+%E0%A4%B9%E0%A5%88+%3F",
            'es': "%C2%BFQu%C3%A9+es+steemit+%3F",
            'fr': "Qu%27est-ce+que+steemit+%3F",
            'de': "Was+ist+steemit+%3F",
            'ru': "Что+такое+steemit+%3F",
            'uk': "Що+таке+steemit+%3F",
            'zh': "什么是steemit%3F",
            'ar': "%D9%85%D8%A7+%D9%87%D9%88+steemit%3F"
        }

        query = queries.get(language_code, queries['en'])
        return base_url + query
    
    def ask_copilot(self, language_code):
        base_message = "ask copilot 🤖"
        translations = {
            'it': "chiedi a copilot 🤖",
            'en': "ask copilot 🤖",
            'hi': "कोपिलॉट से पूछें 🤖",
            'es': "pregunta a copilot 🤖",
            'fr': "demande à copilot 🤖",
            'de': "frag copilot 🤖",
            'ru': "спроси у copilot 🤖",
            'uk': "запитай copilot 🤖",
            'zh': "问copilot 🤖",
            'ar': "اسأل copilot 🤖"
        }

        return translations.get(language_code, base_message)
    
    def gif_size_exceeded(self, language_code, max_size):
        eng = f"Sorry... The size of the gif file is more than {max_size}MB.🚫 \nIf you want to increase the capacity, upgrade to the premium plan 💎"
        lang_text = {
            'it': f"Spiacente... Le dimensioni del file gif sono superiori a {max_size}MB.🚫 \nSe vuoi aumentare la capacità, passa al piano premium 💎",
            'en': eng,
            'hi': f"क्षमा करें... GIF फ़ाइल का आकार {max_size}MB से अधिक है।🚫 \nअगर आप क्षमता बढ़ाना चाहते हैं, तो प्रीमियम प्लान पर अपग्रेड करें 💎",
            'es': f"Lo siento... El tamaño del archivo gif es mayor que {max_size}MB.🚫 \nSi deseas aumentar la capacidad, actualiza al plan premium 💎",
            'fr': f"Désolé... La taille du fichier gif est supérieure à {max_size}MB.🚫 \nSi vous souhaitez augmenter la capacité, passez au plan premium 💎",
            'de': f"Entschuldigung... Die Größe der GIF-Datei ist größer als {max_size}MB.🚫 \nWenn Sie die Kapazität erhöhen möchten, wechseln Sie zum Premium-Tarif 💎",
            'ru': f"Извините... Размер файла gif превышает {max_size}MB.🚫 \nЕсли вы хотите увеличить емкость, обновитесь до премиум-плана 💎",
            'uk': f"Вибачте... Розмір файлу gif перевищує {max_size}MB.🚫 \nЯкщо ви хочете збільшити ємність, оновіться до преміум-плану 💎",
            'zh': f"抱歉... GIF 文件的大小超过了 {max_size}MB.🚫 \n如果您想增加容量，请升级到高级套餐 💎",
            'ar': f"آسف... حجم ملف GIF أكبر من {max_size}MB.🚫 \nإذا كنت ترغب في زيادة السعة، فانتقل إلى الخطة المميزة 💎"
        }
        return lang_text.get(language_code, eng)
    
    def post_saved_message(language_code, date_time):
        eng_message = f"The post has been saved and will be published at {date_time}."

        translations = {
            'it': f"Il post è stato salvato e verrà pubblicato alle {date_time}.",
            'en': eng_message,
            'hi': f"पोस्ट सहेजा गया है और {date_time} पर प्रकाशित किया जाएगा।",
            'es': f"La publicación ha sido guardada y se publicará a las {date_time}.",
            'fr': f"Le post a été enregistré et sera publié à {date_time}.",
            'de': f"Der Beitrag wurde gespeichert und wird um {date_time} veröffentlicht.",
            'ru': f"Пост сохранен и будет опубликован в {date_time}.",
            'uk': f"Пост збережено і буде опубліковано о {date_time}.",
            'zh': f"帖子已保存，将于 {date_time} 发布。",
            'ar': f"تم حفظ المنشور وسيتم نشره في {date_time}."
        }

        return translations.get(language_code, eng_message)
    
    def wait_sub_unsub(self, language_code):
        eng_message = "Please wait a few minutes before performing this action again ⏳"
        translations = {
            'it': "Attendi qualche minuto prima di eseguire di nuovo questa azione ⏳",
            'hi': "कृपया इस क्रिया को फिर से करने से पहले कुछ मिनट प्रतीक्षा करें ⏳",
            'es': "Por favor, espere unos minutos antes de realizar esta acción nuevamente ⏳",
            'fr': "Veuillez attendre quelques minutes avant de refaire cette action ⏳",
            'de': "Bitte warten Sie ein paar Minuten, bevor Sie diese Aktion erneut ausführen ⏳",
            'ru': "Пожалуйста, подождите несколько минут, прежде чем повторить это действие ⏳",
            'uk': "Будь ласка, зачекайте кілька хвилин, перш ніж знову виконати цю дію ⏳",
            'zh': "请稍等几分钟再执行此操作 ⏳",
            'ar': "يرجى الانتظار بضع دقائق قبل تنفيذ هذا الإجراء مرة أخرى ⏳"
        }
        return translations.get(language_code, eng_message)
    
    def unsubscribe_message(self, language_code):
        eng_message = "unsubscribe 🚫"
        translations = {
            'it': "annulla l'iscrizione 🚫",
            'hi': "सदस्यता समाप्त करें 🚫",
            'es': "darse de baja 🚫",
            'fr': "se désabonner 🚫",
            'de': "abmelden 🚫",
            'ru': "отписаться 🚫",
            'uk': "відписатися 🚫",
            'zh': "取消订阅 🚫",
            'ar': "إلغاء الاشتراك 🚫"
        }
        return translations.get(language_code, eng_message)
    
    def subscribed_message(self, language_code):
        eng_message = "subscribed ✅"

        translations = {
            'it': "iscritto ✅",
            'hi': "सदस्यता ली गई ✅",
            'es': "suscrito ✅",
            'fr': "abonné ✅",
            'de': "abonniert ✅",
            'ru': "подписан ✅",
            'uk': "підписано ✅",
            'zh': "已订阅 ✅",
            'ar': "مشترك ✅"
        }

        return translations.get(language_code, eng_message)
    
    def subscribe_message(self, language_code):
        eng_message = "subscribe ✅"
        translations = {
            'it': "iscriviti ✅",
            'hi': "सदस्यता लें ✅",
            'es': "suscribirse ✅",
            'fr': "s'abonner ✅",
            'de': "abonnieren ✅",
            'ru': "подписаться ✅",
            'uk': "підписатися ✅",
            'zh': "订阅 ✅",
            'ar': "اشترك ✅"
        }
        return translations.get(language_code, eng_message)
    
    def unsubscribed_message(self, language_code):
        eng_message = "unsubscribed 🚫"

        translations = {
            'it': "annullato l'iscrizione 🚫",
            'hi': "सदस्यता समाप्त 🚫",
            'es': "dado de baja 🚫",
            'fr': "désabonné 🚫",
            'de': "abgemeldet 🚫",
            'ru': "отписался 🚫",
            'uk': "відписано 🚫",
            'zh': "已取消订阅 🚫",
            'ar': "تم إلغاء الاشتراك 🚫"
        }

        return translations.get(language_code, eng_message)

##################################################################################
################################################################################## List

    def get_language_list(self):
        eng = "Language setting 🇬🇧"
        lang_text = {
            'it': "Impostazioni Lingua 🇮🇹",
            'en': eng,
            'hi': "भाषा सेटिंग 🇮🇳",
            'es': "Configuración de Idioma 🇪🇸",
            'fr': "Paramètres de Langue 🇫🇷",
            'de': "Spracheinstellungen 🇩🇪",
            'ru': "Настройки Языка 🇷🇺",
            'uk': "Налаштування Мови 🇺🇦",
            'zh': "语言设置 🇨🇳",
            'ar': "إعداد اللغة 🇸🇦"
        }
        return list(lang_text.values())

    def get_community_search_list(self):
        lang_text = {
            'it': "Cerca comunità 👥",
            'hi': "समुदाय खोजें 👥",
            'es': "Buscar comunidad 👥",
            'fr': "Rechercher une communauté 👥",
            'de': "Community suchen 👥",
            'ru': "Поиск сообщества 👥",
            'uk': "Шукати спільноту 👥",
            'zh': "搜索社区 👥",
            'ar': "البحث عن المجتمع 👥",
            'en': "Search community 👥"  # English
        }
        return list(lang_text.values())
    
    def get_setting_list(self):
        lang_text = {
            'it': "Impostazioni ⚙️",
            'hi': "सेटिंग ⚙️",
            'es': "Configuración ⚙️",
            'fr': "Paramètres ⚙️",
            'de': "Einstellungen ⚙️",
            'ru': "Настройки ⚙️",
            'uk': "Налаштування ⚙️",
            'zh': "设置 ⚙️",
            'ar': "الإعدادات ⚙️",
            'en': "Setting ⚙️"  # English
        }      
        return list(lang_text.values())
    
    def get_create_account_list(self):
        lang_text = {
            'it': "Crea account 🆕",
            'hi': "खाता बनाएं 🆕",
            'es': "Crear cuenta 🆕",
            'fr': "Créer un compte 🆕",
            'de': "Konto erstellen 🆕",
            'ru': "Создать аккаунт 🆕",
            'uk': "Створити акаунт 🆕",
            'zh': "创建账户 🆕",
            'ar': "إنشاء حساب 🆕",
            'en': "Create account 🆕"  # English
        }
        
        return list(lang_text.values())
    
    def get_back_list(self):
        eng = "Back 🔙"
        lang_text = {
            'it': "Indietro 🔙",
            'en': eng,
            'hi': "पीछे 🔙",
            'es': "Volver 🔙",
            'fr': "Retour 🔙",
            'de': "Zurück 🔙",
            'ru': "Назад 🔙",
            'uk': "Назад 🔙",
            'zh': "返回 🔙",
            'ar': "العودة 🔙"
        }
        return list(lang_text.values())