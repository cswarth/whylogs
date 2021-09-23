import warnings

from google.protobuf.wrappers_pb2 import Int64Value

from whylogs.proto import Counters


class CountersTracker:
    """
    Class to keep track of the counts of various data types

    :param count:  Current number of objects
    :type count: int, optional
    :param true_count:  Number of boolean values
    :type true_count: int, optional
    :param null_count:  Number of nulls encountered
    :type null_count: int, optional

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

        :return:  The merged tracker
        :rtype: CountersTracker
        """
        return CountersTracker(
            count=self.count + other.count,
            true_count=self.true_count + other.true_count,
        )

    def to_protobuf(self, null_count=0):
        """
        Return the object serialized as a protobuf message
        """
        opts = dict(count=self.count)
        if self.true_count > 0:
            opts["true_count"] = Int64Value(value=self.true_count)

        # TODO: remove this logic once we deprecate null_count form the protobuf schema
        if null_count > 0:
            opts["null_count"] = Int64Value(value=null_count)
        return Counters(**opts)

    @staticmethod
    def from_protobuf(message: Counters):
        """
        Load from a protobuf message

        :rtype: CountersTracker
        """
        return CountersTracker(
            count=message.count,
            true_count=message.true_count.value,
        )
