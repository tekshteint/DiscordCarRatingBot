set -e

mongo <<EOF
use CarRatingBotDB

db.createUser({
  user: 'discord',
  pwd: 'admin',
  roles: [{ role: 'readWrite', db: 'CarRatingBotDB' }]
});

db.createCollection('fb_collection', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      properties: {
        _id: { bsonType: 'string' },
        Make: { bsonType: 'string', maxLength: 100 },
        Model: { bsonType: 'string', maxLength: 100 },
        Year: { bsonType: 'int' },
        Description: { bsonType: 'string' },
        Location: { bsonType: 'string', maxLength: 100 },
        Price: { bsonType: 'double' }
      }
    }
  }
});

db.createCollection('cl_collection', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      properties: {
        _id: { bsonType: 'string' },
        Make: { bsonType: 'string', maxLength: 100 },
        Model: { bsonType: 'string', maxLength: 100 },
        Year: { bsonType: 'int' },
        Description: { bsonType: 'string' },
        Location: { bsonType: 'string', maxLength: 100 },
        Price: { bsonType: 'double' },
        Vin: { bsonType: 'string', maxLength: 100 },
        Odometer: { bsonType: 'int' },
        Condition: { bsonType: 'string', maxLength: 100 },
        Drive: { bsonType: 'string', maxLength: 100 },
        Fuel: { bsonType: 'string', maxLength: 100 },
        paint_color: { bsonType: 'string', maxLength: 100 },
        size: { bsonType: 'string', maxLength: 100 },
        title_status: { bsonType: 'string', maxLength: 100 },
        transmission: { bsonType: 'string', maxLength: 100 },
        type: { bsonType: 'string', maxLength: 100 }
      }
    }
  }
});

EOF
