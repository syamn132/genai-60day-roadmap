import math


def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))


def magnitude(vector):
    return math.sqrt(
        sum(x * x for x in vector)
    )


def cosine_similarity(a, b):

    numerator = dot_product(a, b)

    denominator = (
        magnitude(a)
        *
        magnitude(b)
    )

    return numerator / denominator


cat = [0.80, 0.20, 0.70]

dog = [0.75, 0.25, 0.68]

car = [-0.40, 0.90, 0.10]


print(
    "cat ↔ dog:",
    cosine_similarity(cat, dog)
)

print(
    "cat ↔ car:",
    cosine_similarity(cat, car)
)