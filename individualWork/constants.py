class TabNames:
    QUAD = "quad"
    GRAPH = "graph"
    INTERSECTION = "intersection"
    CONVERT = "convert"

    @classmethod
    def get_display_names(cls):
        return {
            cls.QUAD: "Квадратное уравнение",
            cls.GRAPH: "График функции",
            cls.INTERSECTION: "Пересечение функций",
            cls.CONVERT: "Перевод систем счисления"
        }