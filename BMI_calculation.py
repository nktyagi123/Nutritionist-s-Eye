class BMI:
    def __init__(self, weight_kg, height_ft, height_inch):
        self.weight_kg = weight_kg
        self.height_ft = height_ft
        self.height_inch = height_inch

    def feet_inch_to_meters(self):
        """
        Convert height from feet and inches to meters.

        Returns:
            float: Height in meters.
        """
        total_inches = self.height_ft * 12 + self.height_inch
        height_m = total_inches * 0.0254  # 1 inch = 0.0254 meters
        return height_m

    def calculate_bmi(self):
        """
        Calculate the Body Mass Index (BMI) of a person.

        Returns:
            float: The calculated BMI value.
        """
        height_m = self.feet_inch_to_meters()
        bmi = self.weight_kg / (height_m ** 2)
        return round(bmi, 2)


