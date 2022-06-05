class Validate:
    @staticmethod
    def ValidateIntValue(value, less_than=False, more_than=False, limit=0):
        try:
            value = int(value)
            if less_than:
                if value < limit:
                    return True
                else:
                    return False
            elif more_than:
                if value > limit:
                    return True
                else:
                    return False
            return True
        except:
            return False

    @staticmethod
    def ValidateExistenceOfIntValue(value, existing_values):
        try:
            value = int(value)
            if value in existing_values:
                return False
            return True
        except:
            return False
