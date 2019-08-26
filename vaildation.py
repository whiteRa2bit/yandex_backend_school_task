class AddCitizensShema(Schema):
    citizen_id = fields.Int(required=True)
    town = fields.Str(required=True)
    street = fields.Str(required=True)
    building = fields.Str(required=True)
    apartment = fields.Int(required=True)
    name = fields.Str(required=True)
    birth_date = fields.Str(required=True)
    gender = fields.Str(required=True)
    relatives = fields.List(fields.Int, required=True)

    @validates('birth_date')
    def is_not_in_future(self, value):  
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")


class ModifyCitizenInfoShema(Schema):
    town = fields.Str(required=False)
    street = fields.Str(required=False)
    building = fields.Str(required=False)
    apartment = fields.Int(required=False)
    name = fields.Str(required=False)
    birth_date = fields.Str(required=False)
    gender = fields.Str(required=False)
    relatives = fields.List(fields.Int, required=True)

add_citizens_schema = AddCitizensShema()
modify_citizen_info_shema = ModifyCitizenInfoShema()
