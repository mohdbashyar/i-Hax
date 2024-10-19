from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Medication model
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

# Create the database tables if they do not exist
with app.app_context():
    db.create_all()
    # Seed the database with sample data
    if Medication.query.count() == 0:  # Only seed if the table is empty
        seed_data()

def seed_data():
    medications_data = {
        "Pain Relief": [
            {"name": "Aspirin", "description": "Pain relief and anti-inflammatory.", "price": 5.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Ibuprofen", "description": "Pain relief and anti-inflammatory.", "price": 7.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Naproxen", "description": "Nonsteroidal anti-inflammatory drug.", "price": 9.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Acetaminophen", "description": "Pain reliever and fever reducer.", "price": 4.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Diclofenac", "description": "Pain relief for arthritis and muscle pain.", "price": 8.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Celecoxib", "description": "Used to treat pain or inflammation.", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Meloxicam", "description": "Used to treat pain or inflammation.", "price": 6.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Ketoprofen", "description": "Used to treat pain and inflammation.", "price": 10.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Etodolac", "description": "Nonsteroidal anti-inflammatory medication.", "price": 8.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Piroxicam", "description": "Used for pain relief in arthritis.", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
        ],
        "Cold & Flu": [
            {"name": "NyQuil", "description": "Cold and flu relief.", "price": 8.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "DayQuil", "description": "Daytime cold relief.", "price": 8.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Robitussin", "description": "Cough relief and chest congestion.", "price": 7.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Theraflu", "description": "Relieves cold and flu symptoms.", "price": 9.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Mucinex", "description": "Relieves chest congestion.", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Sudafed", "description": "Nasal decongestant for sinus relief.", "price": 6.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Zicam", "description": "Cold remedy and nasal relief.", "price": 12.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Vicks Vapor Rub", "description": "Topical ointment for cough relief.", "price": 4.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Alka-Seltzer Plus", "description": "Relieves cold and flu symptoms.", "price": 5.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Claritin-D", "description": "Allergy relief for sinus pressure.", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
        ],
        "Vitamins & Supplements": [
            {"name": "Vitamin C", "description": "Boosts immune system.", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Vitamin D", "description": "Supports bone health.", "price": 10.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Multivitamins", "description": "Daily nutritional supplement.", "price": 14.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Fish Oil", "description": "Omega-3 fatty acids for heart health.", "price": 19.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Calcium", "description": "Supports bone strength.", "price": 8.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Probiotics", "description": "Promotes gut health.", "price": 16.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Iron", "description": "Essential mineral for blood health.", "price": 9.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Folic Acid", "description": "Supports cell growth and metabolism.", "price": 7.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Vitamin B12", "description": "Supports nerve and blood cell health.", "price": 11.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "CoQ10", "description": "Antioxidant for heart health.", "price": 15.99, "image_url": "https://via.placeholder.com/150"},
        ],
        "Digestive Health": [
            {"name": "Protonix", "description": "Reduces stomach acid.", "price": 20.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Pepto-Bismol", "description": "Relieves upset stomach and diarrhea.", "price": 6.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Metamucil", "description": "Fiber supplement for digestive health.", "price": 8.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Lactaid", "description": "Helps digest lactose.", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Miralax", "description": "Osmotic laxative for constipation relief.", "price": 14.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Zantac", "description": "Acid reducer for heartburn relief.", "price": 9.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Gas-X", "description": "Relieves bloating and gas.", "price": 5.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Colace", "description": "Stool softener for constipation.", "price": 7.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Fiber Choice", "description": "Fiber supplement for digestive health.", "price": 10.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Tums", "description": "Antacid for heartburn relief.", "price": 4.99, "image_url": "https://via.placeholder.com/150"},
        ],
        "Skin Care": [
            {"name": "Neutrogena Sunscreen", "description": "SPF 50 for sun protection.", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "CeraVe Moisturizing Cream", "description": "Hydrates and restores the skin barrier.", "price": 12.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Eucerin Healing Lotion", "description": "Relieves dry, sensitive skin.", "price": 8.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Aveeno Daily Moisturizer", "description": "Hydrates and soothes skin.", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Aquaphor Healing Ointment", "description": "Protects and heals dry skin.", "price": 9.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Olay Regenerist Cream", "description": "Anti-aging moisturizer.", "price": 14.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Burt's Bees Lip Balm", "description": "Moisturizes and protects lips.", "price": 3.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Hydrocolloid Bandages", "description": "Protects and promotes healing for minor wounds.", "price": 7.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Retinol Cream", "description": "Reduces fine lines and wrinkles.", "price": 16.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Tea Tree Oil", "description": "Natural remedy for acne.", "price": 10.49, "image_url": "https://via.placeholder.com/150"},
        ],
        "Allergy Relief": [
            {"name": "Claritin", "description": "Non-drowsy allergy relief.", "price": 9.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Benadryl", "description": "Allergy relief with sedative effect.", "price": 7.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Zyrtec", "description": "Allergy relief for sneezing and runny nose.", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Flonase", "description": "Nasal spray for allergy relief.", "price": 13.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Allegra", "description": "Fast relief from allergy symptoms.", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Singulair", "description": "Helps control allergy symptoms.", "price": 15.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "NasalCrom", "description": "Prevents allergic rhinitis symptoms.", "price": 8.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Pataday", "description": "Eye drops for allergy relief.", "price": 14.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Astelin", "description": "Nasal spray for seasonal allergy relief.", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Epinephrine Auto-Injector", "description": "Emergency treatment for severe allergic reactions.", "price": 150.00, "image_url": "https://via.placeholder.com/150"},
        ],
        "Antibiotics": [
            {"name": "Amoxicillin", "description": "Treats a variety of infections.", "price": 15.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Ciprofloxacin", "description": "Broad-spectrum antibiotic.", "price": 18.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Azithromycin", "description": "Used to treat bacterial infections.", "price": 20.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Doxycycline", "description": "Treats bacterial infections and acne.", "price": 17.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Cephalexin", "description": "Antibiotic for infections.", "price": 16.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Clindamycin", "description": "Used for serious infections.", "price": 22.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Metronidazole", "description": "Treats various infections.", "price": 19.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Levofloxacin", "description": "Broad-spectrum antibiotic.", "price": 21.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Trimethoprim/Sulfamethoxazole", "description": "Treats a variety of infections.", "price": 24.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Vancomycin", "description": "Used to treat serious infections.", "price": 50.00, "image_url": "https://via.placeholder.com/150"},
        ],
        "Mental Health": [
            {"name": "Sertraline", "description": "Used to treat depression and anxiety.", "price": 24.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Fluoxetine", "description": "Treats depression, OCD, and panic disorder.", "price": 20.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Escitalopram", "description": "Used for anxiety and depression.", "price": 27.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Citalopram", "description": "Treats depression and anxiety.", "price": 22.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Bupropion", "description": "Used to treat depression and for smoking cessation.", "price": 23.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Venlafaxine", "description": "Used for depression and anxiety.", "price": 28.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Mirtazapine", "description": "Used to treat major depressive disorder.", "price": 26.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Trazodone", "description": "Used for depression and insomnia.", "price": 19.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Aripiprazole", "description": "Used to treat schizophrenia and bipolar disorder.", "price": 29.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Lithium", "description": "Used to treat bipolar disorder.", "price": 30.99, "image_url": "https://via.placeholder.com/150"},
        ],
        "Heart Health": [
            {"name": "Atorvastatin", "description": "Used to lower cholesterol.", "price": 19.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Lisinopril", "description": "Used for high blood pressure.", "price": 14.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Amlodipine", "description": "Treats high blood pressure and angina.", "price": 17.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Metoprolol", "description": "Used for high blood pressure and heart issues.", "price": 16.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Simvastatin", "description": "Used to lower cholesterol.", "price": 18.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Losartan", "description": "Used to treat high blood pressure.", "price": 15.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Clopidogrel", "description": "Helps prevent blood clots.", "price": 23.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Warfarin", "description": "Used to prevent blood clots.", "price": 21.49, "image_url": "https://via.placeholder.com/150"},
            {"name": "Furosemide", "description": "Diuretic for heart failure.", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
            {"name": "Dabigatran", "description": "Used to reduce the risk of stroke.", "price": 32.99, "image_url": "https://via.placeholder.com/150"},
        ]
    }

    for category, medications in medications_data.items():
        for med in medications:
            new_med = Medication(
                name=med['name'],
                category=category,
                description=med['description'],
                price=med['price'],
                image_url=med['image_url']
            )
            db.session.add(new_med)
    db.session.commit()

@app.route('/')
def index():
    medications = Medication.query.all()
    return render_template('index.html', medications=medications)

@app.route('/api/medications', methods=['GET'])
def get_medications():
    medications = Medication.query.all()
    return jsonify([{
        'id': med.id,
        'name': med.name,
        'category': med.category,
        'description': med.description,
        'price': med.price,
        'image_url': med.image_url
    } for med in medications])

@app.route('/api/medications/<int:med_id>', methods=['GET'])
def get_medication(med_id):
    medication = Medication.query.get_or_404(med_id)
    return jsonify({
        'id': medication.id,
        'name': medication.name,
        'category': medication.category,
        'description': medication.description,
        'price': medication.price,
        'image_url': medication.image_url
    })

@app.route('/api/medications', methods=['POST'])
def add_medication():
    data = request.get_json()
    new_med = Medication(
        name=data['name'],
        category=data['category'],
        description=data['description'],
        price=data['price'],
        image_url=data['image_url']
    )
    db.session.add(new_med)
    db.session.commit()
    return jsonify({"message": "Medication added successfully!"}), 201

@app.route('/api/medications/<int:med_id>', methods=['PUT'])
def update_medication(med_id):
    medication = Medication.query.get_or_404(med_id)
    data = request.get_json()
    medication.name = data['name']
    medication.category = data['category']
    medication.description = data['description']
    medication.price = data['price']
    medication.image_url = data['image_url']
    db.session.commit()
    return jsonify({"message": "Medication updated successfully!"})

@app.route('/api/medications/<int:med_id>', methods=['DELETE'])
def delete_medication(med_id):
    medication = Medication.query.get_or_404(med_id)
    db.session.delete(medication)
    db.session.commit()
    return jsonify({"message": "Medication deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
