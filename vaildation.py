from marshmallow import Schema, fields, validates, ValidationError

class CreateNoteInputSchema(Schema):
    citizen_id = fields.Int(required=True)
    town = fields.Str(required=True)
    street = fields.Str(required=True)
    building = fields.Str(required=True)
    apartment = fields.Int(required=True)
    name = fields.Str(required=True)
    birth_date = fields.DateTime(format='%d.%m.%Y', required=True)
    gender = fields.Str(required=True)
    relatives = fields.List(fields.Int, required=True)

    @validates('birth_date')
    def is_not_in_future(value):
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't create notes in the future!")

create_note_schema = CreateNoteInputSchema()
