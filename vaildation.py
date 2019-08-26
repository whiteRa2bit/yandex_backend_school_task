from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from marshmallow.validate import Length, Range
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

    @validates_schema
    def is_appropriate_str_format_town(self, data, **kwargs):
        value = data['town']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
           raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_street(self, data, **kwargs):
        value = data['street']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_building(self, data, **kwargs):
        value = data['building']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")
            

    @validates_schema
    def is_appropriate_gender(self, data, **kwargs):
        value = data['gender']
        if value not in ['male', 'female']:
            raise ValidationError("Can create citizens only with gender 'male' or 'female'")

    @validates_schema
    def is_valid_date(self, data, **kwargs):
        value = data['birth_date'] 
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

    @validates_schema
    def is_appropriate_str_format_town(self, data, **kwargs):
        value = data['town']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
           raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_street(self, data, **kwargs):
        value = data['street']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_building(self, data, **kwargs):
        value = data['building']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")
            

    @validates_schema
    def is_appropriate_gender(self, data, **kwargs):
        value = data['gender']
        if value not in ['male', 'female']:
            raise ValidationError("Can create citizens only with gender 'male' or 'female'")

    @validates_schema
    def is_valid_date(self, data, **kwargs):
        value = data['birth_date'] 
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except:
            raise ValidationError("wrong date format")

        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")

add_citizens_schema = AddCitizensShema()
modify_citizen_info_shema = ModifyCitizenInfoShema()