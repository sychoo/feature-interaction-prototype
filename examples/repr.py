class Sample:
    def __repr__(self):
        """returns a printable representation of the given object."""
        return "__repr__"

    def __str__(self):
        """returns the string representation of the object."""
        return "__str__"

if __name__ == "__main__":
    print(Sample()) # __str__
    print(str(Sample())) # __str__
    print(repr(Sample())) # __repr__