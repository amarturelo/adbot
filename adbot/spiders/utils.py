import string


class Utils:

    @staticmethod
    def join_text(array):
        result = ""
        for item in array:
            s = item

            printable = set(string.printable)
            filter(lambda x: x in printable, s)

            result += s + "\n"

        return result
