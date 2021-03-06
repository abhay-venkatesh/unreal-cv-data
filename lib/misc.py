import re


def colors_match(source_color, target_color, tolerance=3):
    return ((source_color.R >= target_color.R - tolerance
             and source_color.R <= target_color.R + tolerance)
            and (source_color.G >= target_color.G - tolerance
                 and source_color.G <= target_color.G + tolerance)
            and (source_color.B >= target_color.B - tolerance
                 and source_color.B <= target_color.B + tolerance))


class Color(object):
    ''' A utility class to parse color value '''
    regexp = re.compile('\(R=(.*),G=(.*),B=(.*),A=(.*)\)')  # noqa W605

    def __init__(self, color_str):
        self.color_str = color_str
        match = self.regexp.match(color_str)
        (self.R, self.G, self.B,
         self.A) = [int(match.group(i)) for i in range(1, 5)]

    def __repr__(self):
        return self.color_str

    def __eq__(self, other):
        return (self.R == other.R and self.G == other.G and self.B == other.B
                and self.A == other.A)
