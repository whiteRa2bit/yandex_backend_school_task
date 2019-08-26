from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
basedir = os.path.abspath(os.path.dirname(__file__))

class AddCitizensShema(Schema):
    citizen_id = fields.Int(required=True, validate=Range(min=0))
    town = fields.Str(required=True, validate=Length(min=1, max=256))
    street = fields.Str(required=True, validate=Length(min=1, max=256))
    building = fields.Str(required=True, validate=Length(min=1, max=256))
    apartment = fields.Int(required=True, validate=Range(min=0))
    name = fields.Str(required=True, validate=Length(min=1, max=256))
    birth_date = fields.Str(required=True)
    gender = fields.Str(required=True)
    relatives = fields.List(fields.Int, required=True)

    @validates('town')
    def is_appropriate_str_format(self, value):
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates('street')
    def is_appropriate_str_format(self, value):
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates('building')
    def is_appropriate_str_format(self, value):
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")
            

    @validates('gender')
    def is_appropriate_gender(self, value):
        if value not in ['male', 'female']:
            raise ValidationError("Can create citizens only with gender 'male' or 'female'")

    @validates('birth_date')
    def is_valid_date(self, value): 
        """'value' is the datetime parsed from time_created by marshmallow"""
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except:
            raise ValidationError("wrong date format")

        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")


class ModifyCitizenInfoShema(Schema):
    town = fields.Str(required=False, validate=Length(min=1, max=256))
    street = fields.Str(required=False, validate=Length(min=1, max=256))
    building = fields.Str(required=False, validate=Length(min=1, max=256))
    apartment = fields.Int(required=False, validate=Range(min=0))
    name = fields.Str(required=False, validate=Length(min=1, max=256))
    birth_date = fields.Str(required=False)
    gender = fields.Str(required=False)
    relatives = fields.List(fields.Int, required=False)

    @validates('town')
    def is_appropriate_str_format(self, value):
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates('street')
    def is_appropriate_str_format(self, value):
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates('building')
    def is_appropriate_str_format(self, value):
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")
            

    @validates('gender')
    def is_appropriate_gender(self, value):
        if value not in ['male', 'female']:
            raise ValidationError("Can create citizens only with gender 'male' or 'female'")

    @validates('birth_date')
    def is_not_in_future(self, value):  
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")

add_citizens_schema = AddCitizensShema()
modify_citizen_info_shema = ModifyCitizenInfoShema()