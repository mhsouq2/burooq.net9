"""Content bank for the daily E-Sannad promo videos.
Every claim here matches the live product pages on burooq.net/software/ (features and the
AED 1,000 one-time / AED 185 a year from year 2 price). Edit here to change what the videos say."""

SITE = 'https://burooq.net'
WHATSAPP = '056 866 1620'
WHATSAPP_INTL = '971568661620'
PRICE_EN = 'AED 1,000 one time'
PRICE_EN2 = '1st year cloud included · then AED 185/yr'
PRICE_AR = '1,000 درهم مرة واحدة'
PRICE_AR2 = 'السنة الأولى مشمولة · بعدها 185 درهم سنوياً'

# Each product: url slug, accent colour, names, 2-3 hooks (pain), the "old way" label on the
# crossed-out paper, a mock-screen (3 rows), 6 features (EN, AR), hashtags.
P = {}

P['contracting'] = dict(
    slug='construction-erp-uae', color='#c2410c',
    en='Contracting & Projects', ar='برنامج المقاولات والمشاريع',
    hooks=[('Is your project making money... or losing it?', 'مشروعك يربح... ولا يخسر؟'),
           ('Project costs lost in Excel and receipts?', 'تكاليف المشاريع ضايعة بين الإكسل والفواتير؟'),
           ('You only know the profit after the project ends?', 'تعرف الربح بس بعد ما يخلص المشروع؟')],
    old=('Excel', 'إكسل'),
    screen=[('Villa project · Budget', '120,000'), ('Spent so far', '84,300'), ('Expected profit', '+22,500')],
    features=[('Budget vs actual cost', 'الميزانية مقابل التكلفة الفعلية'),
              ('Purchases per project', 'المشتريات على كل مشروع'),
              ('Labour & subcontractors', 'العمالة ومقاولو الباطن'),
              ('Invoices with your logo', 'فواتير بشعار شركتك'),
              ('Contracts & documents', 'العقود والمستندات'),
              ('Profit report per project', 'تقرير ربح كل مشروع')],
    tags='#contracting #constructionuae #projectmanagement #contractors #uaebusiness #abudhabi #dubai #erp #مقاولات #شركات_مقاولات #ابوظبي #دبي #الامارات')

P['retail'] = dict(
    slug='retail-pos', color='#1d4ed8',
    en='Retail Shop POS', ar='نظام كاشير للمحلات',
    hooks=[('Does your cash drawer match at night?', 'الدرج يطابق المبيعات آخر اليوم؟'),
           ('Customers ask for items you ran out of?', 'الزبون يطلب شي وتكتشف إنه خلص؟')],
    old=('Notebook', 'دفتر'),
    screen=[('Today sales', '3,480'), ('Items low in stock', '6'), ('Customer credit', '1,250')],
    features=[('Fast barcode checkout', 'بيع سريع بالباركود'),
              ('Stock levels & low stock', 'المخزون والنواقص'),
              ('Customer credit accounts', 'حسابات الآجل للزبائن'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Supplier purchases', 'المشتريات من الموردين'),
              ('Cashier logins', 'دخول خاص لكل كاشير')],
    tags='#pos #pointofsale #retailshop #shopowner #barcode #uaebusiness #abudhabi #dubai #كاشير #نقاط_البيع #محلات #ابوظبي #دبي')

P['grocery'] = dict(
    slug='grocery-pos', color='#15803d',
    en='Grocery & Supermarket POS', ar='نظام كاشير للبقالات والسوبرماركت',
    hooks=[('Long queue at the counter?', 'طابور طويل عند الكاشير؟'),
           ('Credit customers written in a notebook?', 'حسابات الآجل مكتوبة في دفتر؟')],
    old=('Notebook', 'دفتر'),
    screen=[('Today sales', '5,920'), ('Credit to collect', '2,140'), ('Low stock items', '11')],
    features=[('Barcode & quick buttons', 'باركود وأزرار سريعة'),
              ('Customer credit (aajil)', 'حسابات الآجل'),
              ('Stock & reorder', 'المخزون وإعادة الطلب'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Supplier purchases', 'المشتريات من الموردين'),
              ('Phone & WhatsApp orders', 'طلبات الهاتف والواتساب')],
    tags='#grocery #supermarket #baqala #pos #uaebusiness #abudhabi #dubai #بقالة #سوبرماركت #كاشير #ابوظبي #دبي #الامارات')

P['salon'] = dict(
    slug='salon-pos', color='#be185d',
    en='Salon & Barber Software', ar='برنامج الصالونات والحلاقة',
    hooks=[('Who did the most services today?', 'مين سوّى أكثر خدمات اليوم؟'),
           ('Appointments and payments on paper?', 'المواعيد والمدفوعات على ورق؟')],
    old=('Paper', 'ورق'),
    screen=[('Today services', '38'), ('Top staff', 'Sara · 12'), ('Today income', '4,150')],
    features=[('Services price list', 'قائمة أسعار الخدمات'),
              ('Sales per staff member', 'مبيعات كل موظف'),
              ('Customer history', 'سجل كل عميل'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Receipts with your logo', 'إيصالات بشعارك'),
              ('Appointments & walk-ins', 'المواعيد والزبائن بدون موعد')],
    tags='#salon #beautysalon #barbershop #salonowner #uaebusiness #abudhabi #dubai #صالون #صالون_نسائي #حلاق #ابوظبي #دبي')

P['tailoring'] = dict(
    slug='tailoring-software', color='#7c3aed',
    en='Tailoring Shop Software', ar='برنامج محلات الخياطة',
    hooks=[('Lost a customer\'s measurements again?', 'ضيّعت مقاسات الزبون مرة ثانية؟'),
           ('Which orders are due tomorrow?', 'أي طلبات موعدها بكرة؟')],
    old=('Notebook', 'دفتر'),
    screen=[('Orders due tomorrow', '9'), ('Ready for pickup', '14'), ('Balance to collect', '2,600')],
    features=[('Orders with measurements', 'الطلبات مع المقاسات'),
              ('Orders & due dates', 'الطلبات ومواعيد التسليم'),
              ('Advance & balance', 'العربون والمتبقي'),
              ('Receipts with your logo', 'إيصالات بشعارك'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Customer history', 'سجل كل زبون')],
    tags='#tailoring #tailorshop #abaya #kandura #uaebusiness #abudhabi #dubai #خياطة #خياط #عبايات #كندورة #ابوظبي #دبي')

P['restaurant'] = dict(
    slug='restaurant-pos', color='#b91c1c',
    en='Restaurant & Café POS', ar='نظام كاشير للمطاعم والكافيهات',
    hooks=[('Orders mixed up in the kitchen?', 'الطلبات تتلخبط في المطبخ؟'),
           ('Rush hour and the cashier is slow?', 'وقت الزحمة والكاشير بطيء؟')],
    old=('Paper', 'ورق'),
    screen=[('Open orders', '7'), ('Today sales', '6,780'), ('Takeaway orders', '12')],
    features=[('Fast order taking', 'أخذ الطلبات بسرعة'),
              ('Dine-in, takeaway, delivery', 'محلي، سفري، توصيل'),
              ('Kitchen order tickets', 'طباعة طلبات المطبخ'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Menu with modifiers', 'منيو مع الإضافات'),
              ('Receipts with your logo', 'إيصالات بشعارك')],
    tags='#restaurant #cafe #restaurantpos #cafeowner #foodbusiness #uaebusiness #abudhabi #dubai #مطاعم #كافيه #كاشير #ابوظبي #دبي')

P['emenu'] = dict(
    slug='qr-e-menu', color='#9a3412',
    en='QR E-Menu', ar='المنيو الإلكتروني QR',
    hooks=[('Still reprinting your menu?', 'ما زلت تطبع المنيو من جديد؟'),
           ('Prices changed? Print again?', 'تغيّرت الأسعار؟ تطبع من جديد؟'),
           ('Want orders straight to WhatsApp?', 'تبي الطلبات توصلك على الواتساب؟')],
    old=('Paper menu', 'منيو ورقي'),
    screen=[('Spanish Latte', '18'), ('Saffron Karak', '8'), ('Pistachio Croissant', '22')],
    features=[('Scan QR, see photos & prices', 'امسح وشاهد الصور والأسعار'),
              ('Arabic & English menu', 'منيو عربي وإنجليزي'),
              ('Change prices any time', 'غيّر الأسعار أي وقت'),
              ('Orders to your WhatsApp', 'الطلبات على الواتساب'),
              ('Customer sends location', 'الزبون يرسل موقعه'),
              ('No reprinting costs', 'بدون تكاليف طباعة')],
    tags='#qrmenu #emenu #digitalmenu #restaurant #cafe #uaebusiness #abudhabi #dubai #منيو_الكتروني #منيو #مطاعم #كافيه #ابوظبي #دبي')

P['laundry'] = dict(
    slug='laundry-management-software', color='#0e7490',
    en='Laundry Software', ar='برنامج المغاسل',
    hooks=[('Which customer\'s clothes are ready?', 'ملابس أي زبون جاهزة؟'),
           ('Lost tickets, angry customers?', 'إيصالات ضايعة وزبائن زعلانين؟')],
    old=('Paper tickets', 'إيصالات ورق'),
    screen=[('Orders in process', '23'), ('Ready for pickup', '17'), ('Today income', '1,940')],
    features=[('Orders & item tickets', 'الطلبات وإيصالات القطع'),
              ('Ready / delivered status', 'حالة جاهز / مُسلَّم'),
              ('Company accounts', 'حسابات الشركات'),
              ('Receipts with your logo', 'إيصالات بشعارك'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Delivery', 'التوصيل')],
    tags='#laundry #drycleaning #laundryshop #uaebusiness #abudhabi #dubai #مغسلة #مغاسل #غسيل_ملابس #ابوظبي #دبي #الامارات')

P['carwash'] = dict(
    slug='car-wash-pos', color='#0369a1',
    en='Car Wash POS', ar='نظام كاشير لمغاسل السيارات',
    hooks=[('How many cars did you wash today?', 'كم سيارة غسلت اليوم؟'),
           ('Cash at the car wash not adding up?', 'الكاش في المغسلة ما يطابق؟')],
    old=('Notebook', 'دفتر'),
    screen=[('Cars today', '46'), ('Today income', '2,310'), ('Monthly packages', '18')],
    features=[('Fast sale at the counter', 'بيع سريع'),
              ('Plate number on invoice', 'رقم اللوحة في الفاتورة'),
              ('Monthly packages', 'الباقات الشهرية'),
              ('Company accounts', 'حسابات الشركات'),
              ('Daily closing report', 'تقرير التقفيل اليومي'),
              ('Receipts with your logo', 'إيصالات بشعارك')],
    tags='#carwash #carwashbusiness #carcare #uaebusiness #abudhabi #dubai #مغسلة_سيارات #غسيل_سيارات #ابوظبي #دبي #الامارات')

P['fleet'] = dict(
    slug='fleet-management-software', color='#0f766e',
    en='Fleet & Traffic Fines', ar='إدارة الأسطول والمخالفات',
    hooks=[('Which car is making money?', 'أي سيارة فعلاً تربح؟'),
           ('Traffic fines piling up per car?', 'المخالفات تتراكم على السيارات؟')],
    old=('Excel', 'إكسل'),
    screen=[('Unpaid fines', '3,400'), ('Car 12 · profit', '+4,850'), ('Driver earnings', '27 drivers')],
    features=[('Fines per vehicle', 'المخالفات لكل مركبة'),
              ('Expenses vs income', 'المصاريف مقابل الدخل'),
              ('Driver earnings', 'أرباح السائقين'),
              ('Invoices with your logo', 'فواتير بشعار شركتك'),
              ('Vehicle documents', 'مستندات المركبات'),
              ('Users & permissions', 'مستخدمون وصلاحيات')],
    tags='#fleetmanagement #rentacar #limousine #transport #trafficfines #uaebusiness #abudhabi #dubai #تأجير_سيارات #ليموزين #نقل #ابوظبي #دبي')

# The order the days rotate through: the three things the owner asked to push most
# (contracting, shop POS, e-menu) come up most often.
ROTATION = ['contracting', 'retail', 'emenu', 'grocery', 'contracting', 'salon', 'emenu',
            'restaurant', 'contracting', 'tailoring', 'emenu', 'laundry', 'carwash', 'fleet']


# First-second hook (who it is for) and the honest urgency line (cost of waiting). No fake deadlines.
P['contracting'].update(call=('Contractors!', 'أصحاب شركات المقاولات!'), loss=("Every week without numbers is profit you can't see.", 'كل أسبوع بدون أرقام = ربح ما تشوفه.'))
P['retail'].update(call=('Shop owners!', 'أصحاب المحلات!'), loss=('Every day without a system, money leaks from the drawer.', 'كل يوم بدون نظام، فلوس تضيع من الدرج.'))
P['grocery'].update(call=('Grocery owners!', 'أصحاب البقالات!'), loss=('Every unpaid credit you forget is your money.', 'كل آجل تنساه هو من فلوسك.'))
P['salon'].update(call=('Salon owners!', 'أصحاب الصالونات!'), loss=('Every day on paper, you guess instead of know.', 'كل يوم على الورق، تخمّن بدل ما تعرف.'))
P['tailoring'].update(call=('Tailor shops!', 'أصحاب محلات الخياطة!'), loss=('One lost order = one lost customer.', 'طلب واحد ضايع = زبون ضايع.'))
P['restaurant'].update(call=('Restaurant owners!', 'أصحاب المطاعم!'), loss=('Every wrong order costs you food and customers.', 'كل طلب غلط يكلّفك أكل وزبائن.'))
P['emenu'].update(call=('Restaurants & cafés!', 'المطاعم والكافيهات!'), loss=('Every reprint is money thrown away.', 'كل طباعة جديدة فلوس ضايعة.'))
P['laundry'].update(call=('Laundry owners!', 'أصحاب المغاسل!'), loss=('Every lost ticket = an angry customer.', 'كل إيصال ضايع = زبون زعلان.'))
P['carwash'].update(call=('Car wash owners!', 'أصحاب مغاسل السيارات!'), loss=("Every car not recorded is cash you can't track.", 'كل سيارة ما تسجّلها = كاش ما تقدر تتابعه.'))
P['fleet'].update(call=('Rent-a-car & transport!', 'شركات التأجير والنقل!'), loss=("Fines you don't track = surprises later.", 'مخالفات ما تتابعها = مفاجآت بعدين.'))

START = ('Start today', 'ابدأ اليوم')
# Real calendar moments only (month -> line). Shown in place of START in those months.
SEASON = {12: ('Start 2027 organised', 'ابدأ 2027 بشغلك مرتب'), 1: ('Make this year organised', 'خلّ هالسنة شغلك مرتب')}
