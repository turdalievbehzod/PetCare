"""
Usage:
    python manage.py seed_demo          # insert demo data (skips existing)
    python manage.py seed_demo --clear  # wipe seeded records first, then re-seed
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed realistic veterinary demo data for all content apps."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing seeded records before re-seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear()

        self._seed_contact_info()
        self._seed_contact_inquiries()
        self._seed_about()
        self._seed_team()
        self._seed_services()
        author = self._seed_author()
        self._seed_blogs(author)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _ok(self, label):
        self.stdout.write(f"  {self.style.SUCCESS('[OK]')} {label}")

    def _skip(self, label):
        self.stdout.write(f"  {self.style.WARNING('[--]')} {label} (already exists, skipped)")

    # ------------------------------------------------------------------
    # Clear
    # ------------------------------------------------------------------

    def _clear(self):
        from apps.about.models import AboutPage, TeamMember
        from apps.blogs.models import Blog, BlogCategory
        from apps.contact.models import ContactInfo, ContactInquiry
        from apps.services.models import Service

        Blog.objects.all().delete()
        BlogCategory.objects.all().delete()
        Service.objects.all().delete()
        AboutPage.objects.all().delete()
        TeamMember.objects.all().delete()
        ContactInfo.objects.filter(email="info@pawsandcare.vet").delete()
        ContactInquiry.objects.filter(email__endswith="@demo.vet").delete()
        self.stdout.write(self.style.WARNING("Existing demo records cleared."))

    # ------------------------------------------------------------------
    # Contact info
    # ------------------------------------------------------------------

    def _seed_contact_info(self):
        from apps.contact.models import ContactInfo

        obj, created = ContactInfo.objects.get_or_create(
            email="info@pawsandcare.vet",
            defaults=dict(
                address="14 Veterinary Lane, Greenfield, CA 90210",
                phone="+1 (555) 748-2900",
                working_hours="Mon – Fri  8 am – 7 pm  |  Sat  9 am – 4 pm",
                map_embed_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3153.0!2d-122.4!3d37.7!",
                is_active=True,
            ),
        )
        (self._ok if created else self._skip)("ContactInfo — Paws & Care Vet Clinic")

    # ------------------------------------------------------------------
    # Contact inquiries
    # ------------------------------------------------------------------

    def _seed_contact_inquiries(self):
        from apps.contact.models import ContactInquiry

        inquiries = [
            dict(
                name="Rachel Torres",
                email="rachel.torres@demo.vet",
                phone="+1 (555) 201-3344",
                subject="Appointment for annual check-up",
                message=(
                    "Hi, I'd like to book an annual wellness check for my 3-year-old golden retriever, Max. "
                    "He's due for his boosters and a general health assessment. "
                    "Could you let me know your earliest available slot this week?"
                ),
                is_read=False,
            ),
            dict(
                name="David Kim",
                email="david.kim@demo.vet",
                phone="+1 (555) 387-9920",
                subject="Emergency — cat not eating for 3 days",
                message=(
                    "My cat Luna has completely refused food for three days and is very lethargic. "
                    "She's a 7-year-old Persian and has never done this before. "
                    "Is there an emergency slot today or tomorrow? I'm very worried."
                ),
                is_read=True,
            ),
            dict(
                name="Sofia Hernandez",
                email="sofia.h@demo.vet",
                phone="+1 (555) 456-7890",
                subject="Question about dental cleaning procedure",
                message=(
                    "Hello, I noticed my beagle Charlie has quite a bit of tartar build-up and occasional bad breath. "
                    "Could you explain the dental cleaning process, what anaesthesia is used, "
                    "and roughly how much the procedure costs? Thank you!"
                ),
                is_read=False,
            ),
        ]

        for data in inquiries:
            _, created = ContactInquiry.objects.get_or_create(
                email=data["email"], defaults=data
            )
            (self._ok if created else self._skip)(f"ContactInquiry — {data['name']}")

    # ------------------------------------------------------------------
    # About page
    # ------------------------------------------------------------------

    def _seed_about(self):
        from apps.about.models import AboutPage

        obj, created = AboutPage.objects.get_or_create(
            is_active=True,
            defaults=dict(
                mission_title="Our Mission",
                mission_content=(
                    "At Paws & Care Veterinary Clinic, our mission is to provide compassionate, "
                    "evidence-based medical care for every animal that walks through our door. "
                    "We believe every pet deserves the same level of attention and expertise "
                    "regardless of size or species — from a rescue kitten to a senior Labrador. "
                    "We partner with pet owners to create personalised health plans that keep "
                    "their companions happy, healthy, and thriving at every stage of life."
                ),
                vision_title="Our Vision",
                vision_content=(
                    "We envision a community where every pet receives proactive, preventive care "
                    "and where pet owners feel fully supported and informed. "
                    "By combining the latest veterinary technology with genuine warmth and empathy, "
                    "we aim to be the most trusted animal health partner in the region. "
                    "Our goal is not just to treat illness, but to build lifelong bonds between "
                    "our team, your family, and your pet."
                ),
                commitment_title="We Are Committed to Better Care",
                commitment_description=(
                    "Our team of board-certified veterinarians and licensed technicians invest "
                    "continuously in education and state-of-the-art diagnostics. "
                    "We maintain a fear-free practice environment, use only evidence-based treatments, "
                    "and are available for emergency consultations six days a week."
                ),
                stat1_value=4800,
                stat1_label="Successful Treatments",
                stat2_value=2100,
                stat2_label="Happy Pet Families",
            ),
        )
        (self._ok if created else self._skip)("AboutPage — Paws & Care")

    # ------------------------------------------------------------------
    # Team members
    # ------------------------------------------------------------------

    def _seed_team(self):
        from apps.about.models import TeamMember

        members = [
            dict(
                name="Dr. Sarah Mitchell",
                title="Chief Veterinarian & Founder",
                bio=(
                    "Dr. Mitchell has over 18 years of experience in small-animal medicine "
                    "and surgery. She completed her DVM at UC Davis and a residency in "
                    "internal medicine at Cornell. She founded Paws & Care in 2009 with a "
                    "single belief: that veterinary excellence and genuine compassion go hand in hand."
                ),
                order=1,
                is_active=True,
            ),
            dict(
                name="Dr. James Nguyen",
                title="Small Animal Specialist",
                bio=(
                    "Dr. Nguyen specialises in exotic and small-animal care, with particular "
                    "expertise in feline medicine and rabbit health. He holds a certificate "
                    "in feline practice from the ABVP and is a regular speaker at regional "
                    "veterinary conferences."
                ),
                order=2,
                is_active=True,
            ),
            dict(
                name="Dr. Emily Clarke",
                title="Veterinary Surgeon",
                bio=(
                    "Dr. Clarke is our lead surgeon, with a focus on orthopaedic and soft-tissue "
                    "procedures. After completing her surgical residency in Melbourne, she joined "
                    "Paws & Care in 2016. She has performed over 1,500 successful surgeries and "
                    "is known for her calm, reassuring manner with anxious patients."
                ),
                order=3,
                is_active=True,
            ),
            dict(
                name="Olivia Santos",
                title="Head Veterinary Nurse",
                bio=(
                    "With 12 years of nursing experience, Olivia leads our clinical support team "
                    "and oversees patient recovery and post-operative care. She is certified in "
                    "veterinary anaesthesia monitoring and runs our monthly pet-owner education workshops."
                ),
                order=4,
                is_active=True,
            ),
        ]

        for data in members:
            _, created = TeamMember.objects.get_or_create(name=data["name"], defaults=data)
            (self._ok if created else self._skip)(f"TeamMember — {data['name']}")

    # ------------------------------------------------------------------
    # Services
    # ------------------------------------------------------------------

    def _seed_services(self):
        from apps.services.models import Service

        services = [
            dict(
                title="General Wellness Consultations",
                description=(
                    "Comprehensive nose-to-tail health examinations for pets of all ages. "
                    "Our vets assess weight, coat, dental health, organ function, and behaviour "
                    "to catch problems early and keep your companion in peak condition."
                ),
                icon_class="flaticon-stethoscope",
                order=1,
            ),
            dict(
                title="Vaccination & Immunisation",
                description=(
                    "Protect your pet against preventable diseases with our tailored vaccination "
                    "schedules for puppies, kittens, and adult animals. We follow the latest WSAVA "
                    "guidelines to ensure safe, effective immunisation at every life stage."
                ),
                icon_class="flaticon-syringe",
                order=2,
            ),
            dict(
                title="Dental Care & Cleaning",
                description=(
                    "Periodontal disease is the most common health problem in dogs and cats. "
                    "Our dental team provides professional scaling, polishing, and tooth extractions "
                    "under safe, closely monitored anaesthesia, plus take-home care advice."
                ),
                icon_class="flaticon-tooth",
                order=3,
            ),
            dict(
                title="Surgery & Anaesthesia",
                description=(
                    "From routine desexing to complex orthopaedic repairs, our surgical suite "
                    "is equipped with modern anaesthetic monitoring and heated recovery areas. "
                    "Every patient receives an individual anaesthesia plan reviewed by our surgeon."
                ),
                icon_class="flaticon-scalpel",
                order=4,
            ),
            dict(
                title="Diagnostics & In-House Lab",
                description=(
                    "Fast, accurate results with our on-site digital X-ray, ultrasound, and "
                    "full blood-chemistry analyser. Same-day results mean faster diagnoses and "
                    "quicker treatment for your pet when it matters most."
                ),
                icon_class="flaticon-microscope",
                order=5,
            ),
            dict(
                title="Emergency & After-Hours Care",
                description=(
                    "Accidents and sudden illness don't keep office hours. We offer emergency "
                    "consultations six days a week and maintain an on-call line for after-hours "
                    "triage advice. Your pet's safety is always our top priority."
                ),
                icon_class="flaticon-first-aid-kit",
                order=6,
            ),
        ]

        for data in services:
            _, created = Service.objects.get_or_create(title=data["title"], defaults=data)
            (self._ok if created else self._skip)(f"Service — {data['title']}")

    # ------------------------------------------------------------------
    # Demo author
    # ------------------------------------------------------------------

    def _seed_author(self):
        from apps.users.models import User

        phone = "+15550000001"
        user, created = User.objects.get_or_create(
            phone_number=phone,
            defaults=dict(
                first_name="Editorial",
                last_name="Team",
                email="editorial@pawsandcare.vet",
                is_active=True,
                is_staff=True,
            ),
        )
        if created:
            user.set_password("PawsDemo2025!")
            user.save(update_fields=["password"])
            self._ok("Demo author — Editorial Team")
        else:
            self._skip("Demo author — Editorial Team")
        return user

    # ------------------------------------------------------------------
    # Blog categories + posts
    # ------------------------------------------------------------------

    def _seed_blogs(self, author):
        from apps.blogs.models import Blog, BlogCategory

        categories_data = [
            ("Pet Health & Wellness", "pet-health-wellness"),
            ("Nutrition & Diet", "nutrition-diet"),
            ("Preventive Care", "preventive-care"),
            ("Pet Behaviour", "pet-behaviour"),
        ]

        cats = {}
        for name, slug in categories_data:
            obj, created = BlogCategory.objects.get_or_create(
                slug=slug, defaults={"name": name}
            )
            cats[slug] = obj
            (self._ok if created else self._skip)(f"BlogCategory — {name}")

        now = timezone.now()

        posts = [
            dict(
                title="10 Warning Signs Your Dog Needs to See a Vet",
                slug="10-warning-signs-your-dog-needs-to-see-a-vet",
                excerpt=(
                    "Dogs can't tell us when something's wrong, so it's up to us to spot the signs. "
                    "Here are ten symptoms that should never be ignored."
                ),
                content="""<p>As devoted pet owners, we know our dogs better than anyone. But even the most observant owner can miss subtle signs of illness. Being aware of these ten warning signs can make the difference between early treatment and a serious health crisis.</p>

<h3>1. Sudden Loss of Appetite</h3>
<p>A dog that refuses food for more than 24 hours — especially one that normally inhales their meals — warrants a call to your vet. Appetite loss can indicate anything from a simple stomach upset to kidney disease or pain.</p>

<h3>2. Excessive Thirst or Urination</h3>
<p>Drinking or urinating significantly more than usual can be an early indicator of diabetes, Cushing's disease, or kidney failure. Keep an eye on the water bowl and litter habits.</p>

<h3>3. Lethargy or Sudden Disinterest in Play</h3>
<p>Every dog has off days, but two or more consecutive days of unusual tiredness, reluctance to walk, or disinterest in their favourite toys is a red flag worth investigating.</p>

<h3>4. Vomiting or Diarrhoea Lasting More Than 24 Hours</h3>
<p>Occasional vomiting happens. Persistent vomiting or diarrhoea — particularly with blood — is an emergency. Dehydration sets in quickly, especially in smaller breeds.</p>

<h3>5. Difficulty Breathing</h3>
<p>Laboured breathing, open-mouth panting at rest, or a persistent cough are never normal. These can indicate heart disease, pneumonia, or an allergic reaction.</p>

<h3>6. Limping or Difficulty Rising</h3>
<p>While dogs can sprain muscles like humans, persistent limping lasting more than a day, or difficulty getting up from a lying position, may signal arthritis, a ligament tear, or a fracture.</p>

<h3>7. Changes in Eye or Nose Discharge</h3>
<p>Clear eye discharge is often normal. Yellow, green, or thick discharge from the eyes or nose points to infection and needs attention.</p>

<h3>8. Bloated or Distended Abdomen</h3>
<p>A suddenly swollen belly — especially accompanied by unproductive retching — can indicate bloat (GDV), a life-threatening condition that requires immediate veterinary care.</p>

<h3>9. Unexplained Weight Loss</h3>
<p>Significant weight loss over a few weeks without a change in diet is a serious symptom. Cancer, intestinal parasites, diabetes, and hyperthyroidism are all possible causes.</p>

<h3>10. Unusual Lumps or Skin Changes</h3>
<p>Not every lump is dangerous, but any new growth should be checked, particularly if it changes size or shape rapidly. Early detection is the single best tool against cancer.</p>

<p><strong>When in doubt, call us.</strong> We would always rather reassure you that everything is fine than have you wait too long on something serious. Your dog's health is our priority.</p>""",
                category=cats["pet-health-wellness"],
                tags="dog health,symptoms,emergency,wellness",
                views_count=312,
                is_published=True,
                published_at=now,
            ),
            dict(
                title="The Best Diet for Cats with Kidney Disease",
                slug="best-diet-cats-kidney-disease",
                excerpt=(
                    "Chronic kidney disease affects roughly 1 in 3 cats over 12 years old. "
                    "The right nutrition can slow its progression and significantly improve quality of life."
                ),
                content="""<p>Feline chronic kidney disease (CKD) is one of the most common conditions we see in older cats. While there is no cure, dietary management is one of the most powerful tools we have to slow its progression and keep your cat comfortable for longer.</p>

<h3>Why Diet Matters So Much</h3>
<p>Healthy kidneys filter waste products from the blood. When they lose function, toxins build up. The right diet reduces the kidney's workload and slows the buildup of these harmful byproducts.</p>

<h3>Key Dietary Principles</h3>

<h4>1. Controlled Phosphorus</h4>
<p>Phosphorus is the most critical nutrient to restrict in CKD cats. High phosphorus accelerates kidney damage. Look for therapeutic renal diets — not just "senior" foods — with phosphorus levels below 0.5% dry matter.</p>

<h4>2. Moderate, High-Quality Protein</h4>
<p>Old advice said to severely restrict protein. Current evidence suggests moderate restriction with high biological-value protein (chicken, fish, egg) is better. Avoid plant-based proteins, which are harder for cats to utilise.</p>

<h4>3. Hydration Above All</h4>
<p>Cats with CKD dehydrate easily. Wet food is strongly preferred over dry kibble — the moisture content directly supports kidney function. Some cats benefit from a pet water fountain to encourage drinking.</p>

<h4>4. Omega-3 Fatty Acids</h4>
<p>Fish oil supplementation (EPA and DHA) has been shown to reduce inflammation in the kidneys and may slow decline. Ask your vet about appropriate dosing.</p>

<h3>Therapeutic Renal Diets</h3>
<p>Prescription renal diets from brands like Royal Canin Renal, Hill's k/d, and Purina Pro Plan NF are formulated specifically to meet these needs. They typically require a prescription because they are genuinely different from standard cat food — not just marketing.</p>

<h3>Getting a Fussy Cat to Eat</h3>
<p>Many cats dislike sudden diet changes. Transition slowly over 2–4 weeks, mixing increasing amounts of the new food with the old. Warming wet food slightly can make it more appealing.</p>

<p>If you've had your cat diagnosed with CKD, book a nutritional consultation with our team. We'll create a personalised feeding plan based on your cat's stage, weight, and individual preferences.</p>""",
                category=cats["nutrition-diet"],
                tags="cats,kidney disease,CKD,nutrition,diet",
                views_count=198,
                is_published=True,
                published_at=now,
            ),
            dict(
                title="Why Annual Vaccinations Are Still Essential for Adult Pets",
                slug="why-annual-vaccinations-essential-adult-pets",
                excerpt=(
                    "Many owners assume vaccines are only for puppies and kittens. "
                    "Here's what the science actually says about protecting adult dogs and cats."
                ),
                content="""<p>Vaccination is one of the most effective and affordable ways to protect your pet's life. Yet once the puppy or kitten series is complete, many owners wonder whether annual visits and boosters are truly necessary. The short answer is yes — here's why.</p>

<h3>How Vaccine Immunity Works</h3>
<p>Vaccines teach the immune system to recognise and fight specific pathogens. Over time, this immunity can wane — the rate depends on the individual animal, the specific disease, and the vaccine type.</p>

<h3>Core Vaccines Every Pet Needs</h3>

<h4>Dogs</h4>
<ul>
  <li><strong>Distemper, Hepatitis, Parvovirus (DHPPi):</strong> Core combination. Parvovirus kills within 72 hours and is widespread in soil. Even indoor dogs can be exposed.</li>
  <li><strong>Rabies:</strong> Legally required in most jurisdictions. Fatal and transmissible to humans.</li>
  <li><strong>Leptospirosis:</strong> Recommended annually in most areas. Spread by wildlife urine in soil and water — even garden puddles.</li>
</ul>

<h4>Cats</h4>
<ul>
  <li><strong>Feline Herpesvirus, Calicivirus, Panleukopenia (FVRCP):</strong> Core combination. Panleukopenia is as devastating to cats as parvovirus is to dogs.</li>
  <li><strong>Feline Leukaemia (FeLV):</strong> Recommended for outdoor cats or those in multi-cat households.</li>
</ul>

<h3>Titre Testing as an Alternative</h3>
<p>Antibody titre tests measure actual immune response in your individual pet's blood. Where titres are high, some core vaccines may be safely deferred. We offer titre testing for dogs and can discuss whether it's appropriate for your pet.</p>

<h3>The Annual Visit Is About More Than Vaccines</h3>
<p>Even if your pet doesn't need every booster every year, the annual wellness examination is invaluable. It's the check that catches dental disease, early organ changes, and lumps before they become serious problems.</p>

<p>Contact us to review your pet's vaccination history and build an up-to-date preventive care schedule tailored to their lifestyle.</p>""",
                category=cats["preventive-care"],
                tags="vaccination,immunisation,dogs,cats,preventive care",
                views_count=145,
                is_published=True,
                published_at=now,
            ),
            dict(
                title="Understanding and Managing Separation Anxiety in Dogs",
                slug="understanding-managing-separation-anxiety-dogs",
                excerpt=(
                    "Separation anxiety is more than just bad behaviour — it's genuine distress. "
                    "Learn how to recognise the signs and what you can do to help."
                ),
                content="""<p>Separation anxiety is one of the most common behavioural problems we discuss with dog owners, and one of the most misunderstood. It is not stubbornness or spite — it is a panic response, and it deserves compassionate, structured treatment.</p>

<h3>What Separation Anxiety Looks Like</h3>
<p>Classic signs begin within minutes of the owner leaving and can include:</p>
<ul>
  <li>Destructive chewing (often focused on exits — doors, window frames)</li>
  <li>Excessive barking, howling, or whining</li>
  <li>House soiling despite being fully toilet-trained</li>
  <li>Pacing, drooling, or panting</li>
  <li>Attempts to escape that result in self-injury</li>
</ul>

<h3>Why It Happens</h3>
<p>Dogs are social animals. For some individuals — often those rehomed, adopted from shelters, or who experienced early life instability — being alone triggers a genuine panic response driven by the same neurological pathways as human anxiety disorders.</p>

<h3>What Doesn't Help</h3>
<p>Punishment never works for separation anxiety. The dog is not choosing to misbehave — it is in a state of panic and cannot learn during that state. Rubbing their nose in accidents or scolding them on your return worsens the condition by adding fear to an already anxious dog.</p>

<h3>What Does Help</h3>

<h4>Graduated Desensitisation</h4>
<p>The gold-standard treatment involves systematically exposing your dog to your departure cues (picking up keys, putting on shoes) without actually leaving, then building absence tolerance from seconds to minutes to hours over many weeks.</p>

<h4>Safe Spaces</h4>
<p>A crate or dedicated "calm room" — introduced positively with food and toys, never as punishment — gives your dog a predictable, secure environment.</p>

<h4>Mental and Physical Exercise</h4>
<p>A tired dog copes better. Thirty minutes of vigorous exercise before you leave significantly reduces anxiety expression. Puzzle feeders and frozen Kongs extend mental engagement after you go.</p>

<h4>Medication as a Bridge</h4>
<p>For moderate to severe cases, short- or long-term medication prescribed by your vet can reduce the anxiety ceiling enough for behavioural work to take hold. Medication alone is not a solution, but combined with training it dramatically improves outcomes.</p>

<h3>When to Seek Professional Help</h3>
<p>If your dog is injuring itself or causing significant property damage, please book a behavioural consultation. Our vets can assess severity and refer you to a certified veterinary behaviourist if needed.</p>""",
                category=cats["pet-behaviour"],
                tags="dogs,separation anxiety,behaviour,training",
                views_count=271,
                is_published=True,
                published_at=now,
            ),
            dict(
                title="A Complete Guide to Dental Care for Dogs and Cats",
                slug="complete-guide-dental-care-dogs-cats",
                excerpt=(
                    "Periodontal disease affects over 80% of pets by age three. "
                    "Good dental hygiene at home — combined with professional cleanings — can add years to your pet's life."
                ),
                content="""<p>Bad breath is often laughed off as a quirky pet trait. In reality, it's usually the first visible symptom of periodontal disease — a bacterial infection of the gum tissue that, left untreated, causes tooth loss, chronic pain, and can affect the heart, kidneys, and liver.</p>

<h3>How Dental Disease Progresses</h3>
<ol>
  <li><strong>Plaque:</strong> Soft bacterial film coats teeth within hours of eating.</li>
  <li><strong>Tartar (Calculus):</strong> Within days, plaque mineralises into hard brown tartar that can't be brushed off.</li>
  <li><strong>Gingivitis:</strong> Bacteria inflame the gumline. Gums become red and bleed easily.</li>
  <li><strong>Periodontitis:</strong> Infection spreads below the gumline, destroying the bone anchoring teeth. At this stage, damage is irreversible.</li>
</ol>

<h3>At-Home Dental Care</h3>

<h4>Toothbrushing — The Gold Standard</h4>
<p>Daily brushing with a pet-specific toothbrush and enzymatic toothpaste (never human toothpaste — xylitol is toxic to dogs) is the single most effective home care option. Start slowly: let your pet taste the paste, then progress to short brushing sessions over a few weeks.</p>

<h4>Dental Chews and Diets</h4>
<p>Products carrying the VOHC (Veterinary Oral Health Council) seal have evidence behind them. Hill's t/d dental diet, Greenies, and OraVet chews all meet this standard. Avoid hard nylon chews, raw bones, or antlers — these crack teeth.</p>

<h4>Water Additives and Gels</h4>
<p>For pets that won't tolerate brushing, VOHC-approved water additives and dental gels provide some benefit. They are less effective than brushing but far better than nothing.</p>

<h3>Professional Dental Cleaning</h3>
<p>Professional scaling is performed under general anaesthesia — not because of pain, but because a thorough subgingival clean is impossible in a conscious, moving animal. During the procedure, we also probe every tooth and take full-mouth dental X-rays to detect disease that is invisible above the gumline.</p>

<p>Most pets need a professional clean every 1–3 years depending on breed, diet, and home care. Small breeds and brachycephalic dogs (Pugs, French Bulldogs) typically need more frequent attention.</p>

<h3>Signs Your Pet Needs a Dental Check Now</h3>
<ul>
  <li>Bad breath beyond mild odour</li>
  <li>Brown or yellow tartar on teeth</li>
  <li>Red, swollen, or bleeding gums</li>
  <li>Chewing on one side or reluctance to eat hard food</li>
  <li>Pawing at the mouth or face</li>
</ul>

<p>Book a complimentary dental assessment with our team. We'll give you an honest picture of your pet's oral health and a realistic home care plan that works for both of you.</p>""",
                category=cats["pet-health-wellness"],
                tags="dental care,teeth,dogs,cats,periodontal disease",
                views_count=189,
                is_published=True,
                published_at=now,
            ),
        ]

        for data in posts:
            author_val = author
            data_with_author = {**data, "author": author_val}
            slug = data_with_author.pop("slug")
            _, created = Blog.objects.get_or_create(
                slug=slug, defaults=data_with_author
            )
            (self._ok if created else self._skip)(f"Blog — {data['title'][:55]}…")
