import warnings

from google.protobuf.wrappers_pb2 import Int64Value

from whylogs.proto import Counters


class CountersTracker:
    """
    Class to keep track of the counts of various data types

    Parameters
    ----------
    count : int, optional
        Current number of objects
    true_count : int, optional
        Number of boolean values
    null_count : int, optional
        Number of nulls encountered
    """

    def __init__(self, count=0, true_count=0):
        self.count = count
        self.true_count = true_count

    def increment_count(self):
        """
        Add one to the count of total objects
        """
        self.count += 1

    def increment_bool(self):
        """
        Add one to the boolean count
        """
        self.true_count += 1

    def increment_null(self):
        """
        Add one to the null count
        """
        warnings.warn("This call is a No-OP. Use SchemaTracker.nullCount instead", DeprecationWarning)

    def merge(self, other):
        """
        Merge another counter tracker with this one

        Returns
        -------
        new_tracker : CountersTracker
            The merged tracker
        """
        return CountersTracker(
            count=self.count + other.count,
            true_count=self.true_count + other.true_count,
        )

    def to_protobuf(self):
        """
        Return the object serialized as a protobuf message
        """
        opts = dict(count=self.count)
        if self.true_count > 0:
            opts["true_count"] = Int64Value(value=self.true_count)
        return Counters(**opts)

    @staticmethod
    def from_protobuf(message: Counters):
        """
        Load from a protobuf message

        Returns
        -------
        counters : CountersTracker
        """
        return CountersTracker(
            count=message.count,
            true_count=message.true_count.value,
        )
