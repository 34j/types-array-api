from __future__ import annotations

from abc import abstractmethod
from collections.abc import Buffer as SupportsBufferProtocol
from collections.abc import Sequence
from enum import Enum
from types import EllipsisType as ellipsis
from typing import (
    Any,
    Literal,
    Protocol,
    TypedDict,
    runtime_checkable,
)

from typing_extensions import CapsuleType as PyCapsule
from typing_extensions import Self

inf = float("inf")

Capabilities = TypedDict("Capabilities", {"boolean indexing": bool, "data-dependent shapes": bool})


class DataTypes(TypedDict, total=False):
    bool: Any
    float32: Any
    float64: Any
    complex64: Any
    complex128: Any
    int8: Any
    int16: Any
    int32: Any
    int64: Any
    uint8: Any
    uint16: Any
    uint32: Any
    uint64: Any


DefaultDataTypes = TypedDict("DefaultDataTypes", {"real floating": Any, "complex floating": Any, "integral": Any, "indexing": Any})


@runtime_checkable
class Info[TDevice](Protocol):
    """Namespace returned by `__array_namespace_info__`."""

    def capabilities(self) -> Capabilities: ...

    def default_device(self) -> TDevice: ...

    def default_dtypes(self, *, device: TDevice | None) -> DefaultDataTypes: ...

    def devices(self) -> list[TDevice]: ...

    def dtypes(self, *, device: TDevice | None, kind: str | tuple[str, ...] | None) -> DataTypes: ...


@runtime_checkable
class NestedSequence[T_t_co](Protocol):
    def __getitem__(self, key: int, /) -> T_t_co | NestedSequence[T_t_co]: ...

    def __len__(self, /) -> int: ...


@runtime_checkable
class iinfo_object[TDtype](Protocol):
    """Dataclass returned by `iinfo`."""

    bits: int
    max: int
    min: int
    dtype: TDtype


@runtime_checkable
class finfo_object[TDtype](Protocol):
    """Dataclass returned by `finfo`."""

    bits: int
    eps: float
    max: float
    min: float
    smallest_normal: float
    dtype: TDtype


@runtime_checkable
class Array[TDtype, TDevice](Protocol):
    def __init__(self) -> None:
        """Initialize the attributes for the array object class."""
        ...

    @property
    def dtype(self) -> TDtype:
        """
        Data type of the array elements.

        Returns
        -------
        out: dtype
            array data type.

        """
        ...

    @property
    def device(self) -> TDevice:
        """
        Hardware device the array data resides on.

        Returns
        -------
        out: device
            a ``device`` object (see :ref:`device-support`).

        """
        ...

    @property
    def mT(self) -> Self:
        """
        Transpose of a matrix (or a stack of matrices).

        If an array instance has fewer than two dimensions, an error should be raised.

        Returns
        -------
        out: array
            array whose last two dimensions (axes) are permuted in reverse order relative to original array (i.e., for an array instance having shape ``(..., M, N)``, the returned array must have shape ``(..., N, M)``). The returned array must have the same data type as the original array.

        """
        ...

    @property
    def ndim(self) -> int:
        """
        Number of array dimensions (axes).

        Returns
        -------
        out: int
            number of array dimensions (axes).

        """
        ...

    @property
    def shape(self) -> tuple[int | None, ...]:
        """
        Array dimensions.

        Returns
        -------
        out: Tuple[Optional[int], ...]
            array dimensions. An array dimension must be ``None`` if and only if a dimension is unknown.


        .. note::
           For array libraries having graph-based computational models, array dimensions may be unknown due to data-dependent operations (e.g., boolean indexing; ``A[:, B > 0]``) and thus cannot be statically resolved without knowing array contents.

        .. note::
           The returned value should be a tuple; however, where warranted, an array library may choose to return a custom shape object. If an array library returns a custom shape object, the object must be immutable, must support indexing for dimension retrieval, and must behave similarly to a tuple.

        """
        ...

    @property
    def size(self) -> int | None:
        """
        Number of elements in an array.

        .. note::
           This must equal the product of the array's dimensions.

        Returns
        -------
        out: Optional[int]
            number of elements in an array. The returned value must be ``None`` if and only if one or more array dimensions are unknown.


        .. note::
           For array libraries having graph-based computational models, an array may have unknown dimensions due to data-dependent operations.

        """
        ...

    @property
    def T(self) -> Self:
        """
        Transpose of the array.

        The array instance must be two-dimensional. If the array instance is not two-dimensional, an error should be raised.

        Returns
        -------
        out: array
            two-dimensional array whose first and last dimensions (axes) are permuted in reverse order relative to original array. The returned array must have the same data type as the original array.


        .. note::
           Limiting the transpose to two-dimensional arrays (matrices) deviates from the NumPy et al practice of reversing all axes for arrays having more than two-dimensions. This is intentional, as reversing all axes was found to be problematic (e.g., conflicting with the mathematical definition of a transpose which is limited to matrices; not operating on batches of matrices; et cetera). In order to reverse all axes, one is recommended to use the functional ``permute_dims`` interface found in this specification.

        """
        ...

    def __abs__(self, /) -> Self:
        """
        Calculates the absolute value for each element of an array instance.

        For real-valued input arrays, the element-wise result has the same magnitude as the respective element in ``x`` but has positive sign.

        .. note::
           For signed integer data types, the absolute value of the minimum representable integer is implementation-dependent.

        Parameters
        ----------
        self
            array instance. Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the element-wise absolute value. If ``self`` has a real-valued data type, the returned array must have the same data type as ``self``. If ``self`` has a complex floating-point data type, the returned arrayed must have a real-valued floating-point data type whose precision matches the precision of ``self`` (e.g., if ``self`` is ``complex128``, then the returned array must have a ``float64`` data type).

        Notes
        -----

        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.abs`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __add__(self, other: int | float | complex | Self, /) -> Self:
        """
        Calculates the sum for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance (augend array). Should have a numeric data type.
        other: Union[int, float, complex, array]
            addend array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the element-wise sums. The returned array must have a data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.add`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __and__(self, other: int | bool | Self, /) -> Self:
        """
        Evaluates ``self_i & other_i`` for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance. Should have an integer or boolean data type.
        other: Union[int, bool, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have an integer or boolean data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.bitwise_and`.

        """
        ...

    def __array_namespace__(self, /, *, api_version: str | None = None) -> ArrayNamespace[Self, TDtype, TDevice]:
        """
        Returns an object that has all the array API functions on it.

        Parameters
        ----------
        self
            array instance.
        api_version: Optional[str]
            string representing the version of the array API specification to be returned, in ``'YYYY.MM'`` form, for example, ``'2020.10'``. If it is ``None``, it should return the namespace corresponding to latest version of the array API specification.  If the given version is invalid or not implemented for the given module, an error should be raised. Default: ``None``.

        Returns
        -------
        out: Any
            an object representing the array API namespace. It should have every top-level function defined in the specification as an attribute. It may contain other public names as well, but it is recommended to only include those names that are part of the specification.

        """
        ...

    def __bool__(self, /) -> bool:
        """
        Converts a zero-dimensional array to a Python ``bool`` object.

        Parameters
        ----------
        self
            zero-dimensional array instance.

        Returns
        -------
        out: bool
            a Python ``bool`` object representing the single element of the array.

        Notes
        -----
        **Special cases**

        For real-valued floating-point operands,

        - If ``self`` is ``NaN``, the result is ``True``.
        - If ``self`` is either ``+infinity`` or ``-infinity``, the result is ``True``.
        - If ``self`` is either ``+0`` or ``-0``, the result is ``False``.

        For complex floating-point operands, special cases must be handled as if the operation is implemented as the logical OR of ``bool(real(self))`` and ``bool(imag(self))``.

        **Lazy implementations**

        The Python language requires the return value to be of type ``bool``. Lazy implementations are therefore not able to return any kind of lazy/delayed object here and should raise a ``ValueError`` instead.

        .. versionchanged:: 2022.12
            Added boolean and complex data type support.

        .. versionchanged:: 2023.12
            Allowed lazy implementations to error.

        """
        ...

    def __complex__(self, /) -> complex:
        """
        Converts a zero-dimensional array to a Python ``complex`` object.

        Parameters
        ----------
        self
            zero-dimensional array instance.

        Returns
        -------
        out: complex
            a Python ``complex`` object representing the single element of the array instance.

        Notes
        -----
        **Special cases**

        For boolean operands,

        - If ``self`` is ``True``, the result is ``1+0j``.
        - If ``self`` is ``False``, the result is ``0+0j``.

        For real-valued floating-point operands,

        - If ``self`` is ``NaN``, the result is ``NaN + NaN j``.
        - If ``self`` is ``+infinity``, the result is ``+infinity + 0j``.
        - If ``self`` is ``-infinity``, the result is ``-infinity + 0j``.
        - If ``self`` is a finite number, the result is ``self + 0j``.

        **Lazy implementations**

        The Python language requires the return value to be of type ``complex``. Lazy implementations are therefore not able to return any kind of lazy/delayed object here and should raise a ``ValueError`` instead.

        .. versionadded:: 2022.12

        .. versionchanged:: 2023.12
            Allowed lazy implementations to error.

        """
        ...

    def __dlpack__(self, /, *, stream: int | Any | None = None, max_version: tuple[int, int] | None = None, dl_device: tuple[Enum, int] | None = None, copy: bool | None = None) -> PyCapsule:
        """
        Exports the array for consumption by :func:`~array_api.from_dlpack` as a DLPack capsule.

        Parameters
        ----------
        self
            array instance.
        stream: Optional[Union[int, Any]]
            for CUDA and ROCm, a Python integer representing a pointer to a stream, on devices that support streams. ``stream`` is provided by the consumer to the producer to instruct the producer to ensure that operations can safely be performed on the array (e.g., by inserting a dependency between streams via "wait for event"). The pointer must be an integer larger than or equal to ``-1`` (see below for allowed values on each platform). If ``stream`` is ``-1``, the value may be used by the consumer to signal "producer must not perform any synchronization". The ownership of the stream stays with the consumer. On CPU and other device types without streams, only ``None`` is accepted.

            For other device types which do have a stream, queue, or similar synchronization/ordering mechanism, the most appropriate type to use for ``stream`` is not yet determined. E.g., for SYCL one may want to use an object containing an in-order ``cl::sycl::queue``. This is allowed when libraries agree on such a convention, and may be standardized in a future version of this API standard.

            .. note::
                Support for a ``stream`` value other than ``None`` is optional and implementation-dependent.

            device-specific values of ``stream`` for CUDA:

            - ``None``: producer must assume the legacy default stream (default).
            - ``1``: the legacy default stream.
            - ``2``: the per-thread default stream.
            - ``> 2``: stream number represented as a Python integer.
            - ``0`` is disallowed due to its ambiguity: ``0`` could mean either ``None``, ``1``, or ``2``.

            device-specific values of ``stream`` for ROCm:

            - ``None``: producer must assume the legacy default stream (default).
            - ``0``: the default stream.
            - ``> 2``: stream number represented as a Python integer.
            - Using ``1`` and ``2`` is not supported.

            .. note::
                When ``dl_device`` is provided explicitly, ``stream`` must be a valid
                construct for the specified device type. In particular, when ``kDLCPU``
                is in use, ``stream`` must be ``None`` and a synchronization must be
                performed to ensure data safety.

            .. admonition:: Tip
                :class: important

                It is recommended that implementers explicitly handle streams. If
                they use the legacy default stream, specifying ``1`` (CUDA) or ``0``
                (ROCm) is preferred. ``None`` is a safe default for developers who do
                not want to think about stream handling at all, potentially at the
                cost of more synchronizations than necessary.
        max_version: Optional[tuple[int, int]]
            the maximum DLPack version that the *consumer* (i.e., the caller of
            ``__dlpack__``) supports, in the form of a 2-tuple ``(major, minor)``.
            This method may return a capsule of version ``max_version`` (recommended
            if it does support that), or of a different version.
            This means the consumer must verify the version even when
            `max_version` is passed.
        dl_device: Optional[tuple[enum.Enum, int]]
            the DLPack device type. Default is ``None``, meaning the exported capsule
            should be on the same device as ``self`` is. When specified, the format
            must be a 2-tuple, following that of the return value of :meth:`array.__dlpack_device__`.
            If the device type cannot be handled by the producer, this function must
            raise ``BufferError``.

            The v2023.12 standard only mandates that a compliant library should offer a way for
            ``__dlpack__`` to return a capsule referencing an array whose underlying memory is
            accessible to the Python interpreter (represented by the ``kDLCPU`` enumerator in DLPack).
            If a copy must be made to enable this support but ``copy`` is set to ``False``, the
            function must raise ``BufferError``.

            Other device kinds will be considered for standardization in a future version of this
            API standard.
        copy: Optional[bool]
            boolean indicating whether or not to copy the input. If ``True``, the
            function must always copy (performed by the producer). If ``False``, the
            function must never copy, and raise a ``BufferError`` in case a copy is
            deemed necessary (e.g. if a cross-device data movement is requested, and
            it is not possible without a copy). If ``None``, the function must reuse
            the existing memory buffer if possible and copy otherwise. Default: ``None``.

            When a copy happens, the ``DLPACK_FLAG_BITMASK_IS_COPIED`` flag must be set.

            .. note::
                If a copy happens, and if the consumer-provided ``stream`` and ``dl_device``
                can be understood by the producer, the copy must be performed over ``stream``.

        Returns
        -------
        capsule: PyCapsule
            a DLPack capsule for the array. See :ref:`data-interchange` for details.

        Raises
        ------
        BufferError
            Implementations should raise ``BufferError`` when the data cannot
            be exported as DLPack (e.g., incompatible dtype or strides). Other
            errors are raised when export fails for other reasons (e.g., incorrect
            arguments passed or out of memory).

        Notes
        -----
        The DLPack version scheme is SemVer, where the major DLPack versions
        represent ABI breaks, and minor versions represent ABI-compatible additions
        (e.g., new enum values for new data types or device types).

        The ``max_version`` keyword was introduced in v2023.12, and goes
        together with the ``DLManagedTensorVersioned`` struct added in DLPack
        1.0. This keyword may not be used by consumers until a later time after
        introduction, because producers may implement the support at a different
        point in time.

        It is recommended for the producer to use this logic in the implementation
        of ``__dlpack__``:

        .. code:: python

            if max_version is None:
                # Keep and use the DLPack 0.X implementation
                # Note: from March 2025 onwards (but ideally as late as
                # possible), it's okay to raise BufferError here
            else:
                # We get to produce `DLManagedTensorVersioned` now. Note that
                # our_own_dlpack_version is the max version that the *producer*
                # supports and fills in the `DLManagedTensorVersioned::version`
                # field
                if max_version >= our_own_dlpack_version:
                    # Consumer understands us, just return a Capsule with our max version
                elif max_version[0] == our_own_dlpack_version[0]:
                    # major versions match, we should still be fine here -
                    # return our own max version
                else:
                    # if we're at a higher major version internally, did we
                    # keep an implementation of the older major version around?
                    # For example, if the producer is on DLPack 1.x and the consumer
                    # is 0.y, can the producer still export a capsule containing
                    # DLManagedTensor and not DLManagedTensorVersioned?
                    # If so, use that. Else, the producer should raise a BufferError
                    # here to tell users that the consumer's max_version is too
                    # old to allow the data exchange to happen.

        And this logic for the consumer in :func:`~array_api.from_dlpack`:

        .. code:: python

            try:
                x.__dlpack__(max_version=(1, 0), ...)
                # if it succeeds, store info from the capsule named "dltensor_versioned",
                # and need to set the name to "used_dltensor_versioned" when we're done
            except TypeError:
                x.__dlpack__(...)

        This logic is also applicable to handling of the new ``dl_device`` and ``copy``
        keywords.

        DLPack 1.0 added a flag to indicate that the array is read-only
        (``DLPACK_FLAG_BITMASK_READ_ONLY``). A consumer that does not support
        read-only arrays should ignore this flag (this is preferred over
        raising an exception; the user is then responsible for ensuring the
        memory isn't modified).

        .. versionchanged:: 2022.12
           Added BufferError.

        .. versionchanged:: 2023.12
           Added the ``max_version``, ``dl_device``, and ``copy`` keywords.

        .. versionchanged:: 2023.12
           Added recommendation for handling read-only arrays.

        """
        ...

    def __dlpack_device__(self, /) -> tuple[Enum, int]:
        """
        Returns device type and device ID in DLPack format. Meant for use within :func:`~array_api.from_dlpack`.

        Parameters
        ----------
        self
            array instance.

        Returns
        -------
        device: Tuple[Enum, int]
            a tuple ``(device_type, device_id)`` in DLPack format. Valid device type enum members are:

            ::

              CPU = 1
              CUDA = 2
              CPU_PINNED = 3
              OPENCL = 4
              VULKAN = 7
              METAL = 8
              VPI = 9
              ROCM = 10
              CUDA_MANAGED = 13
              ONE_API = 14

        """
        ...

    def __eq__(self, other: int | float | complex | bool | Self, /) -> Self:  # type: ignore[override]
        """
        Computes the truth value of ``self_i == other_i`` for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance. May have any data type.
        other: Union[int, float, complex, bool, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). May have any data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type of ``bool``.


        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.equal`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __float__(self, /) -> float:
        """
        Converts a zero-dimensional array to a Python ``float`` object.

        .. note::
           Casting integer values outside the representable bounds of Python's float type is not specified and is implementation-dependent.

        Parameters
        ----------
        self
            zero-dimensional array instance. Should have a real-valued or boolean data type. If ``self`` has a complex floating-point data type, the function must raise a ``TypeError``.

        Returns
        -------
        out: float
            a Python ``float`` object representing the single element of the array instance.

        Notes
        -----
        **Special cases**

        For boolean operands,

        - If ``self`` is ``True``, the result is ``1``.
        - If ``self`` is ``False``, the result is ``0``.

        **Lazy implementations**

        The Python language requires the return value to be of type ``float``. Lazy implementations are therefore not able to return any kind of lazy/delayed object here and should raise a ``ValueError`` instead.

        .. versionchanged:: 2022.12
            Added boolean and complex data type support.

        .. versionchanged:: 2023.12
            Allowed lazy implementations to error.

        """
        ...

    def __floordiv__(self, other: int | float | Self, /) -> Self:
        """
        Evaluates ``self_i // other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           For input arrays which promote to an integer data type, the result of division by zero is unspecified and thus implementation-defined.

        Parameters
        ----------
        self
            array instance. Should have a real-valued data type.
        other: Union[int, float, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a real-valued data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.


        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.floor_divide`.

        """
        ...

    def __ge__(self, other: int | float | Self, /) -> Self:
        """
        Computes the truth value of ``self_i >= other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

        Parameters
        ----------
        self
            array instance. Should have a real-valued data type.
        other: Union[int, float, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a real-valued data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type of ``bool``.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.greater_equal`.

        """
        ...

    def __getitem__(self, key: int | slice | ellipsis | None | tuple[int | slice | ellipsis | None, ...] | Self, /) -> Self:
        """
        Returns ``self[key]``.

        See :ref:`indexing` for details on supported indexing semantics.

        Parameters
        ----------
        self
            array instance.
        key: Union[int, slice, ellipsis, None, Tuple[Union[int, slice, ellipsis, None], ...], array]
            index key.

        Returns
        -------
        out: array
            an array containing the accessed value(s). The returned array must have the same data type as ``self``.

        """
        ...

    def __gt__(self, other: int | float | Self, /) -> Self:
        """
        Computes the truth value of ``self_i > other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

        Parameters
        ----------
        self
            array instance. Should have a real-valued data type.
        other: Union[int, float, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a real-valued data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type of ``bool``.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.greater`.

        """
        ...

    def __index__(self, /) -> int:
        """
        Converts a zero-dimensional integer array to a Python ``int`` object.

        .. note::
           This method is called to implement `operator.index() <https://docs.python.org/3/reference/datamodel.html#object.__index__>`_. See also `PEP 357 <https://www.python.org/dev/peps/pep-0357/>`_.

        Parameters
        ----------
        self
            zero-dimensional array instance. Should have an integer data type. If ``self`` has a floating-point data type, the function must raise a ``TypeError``.

        Returns
        -------
        out: int
            a Python ``int`` object representing the single element of the array instance.

        Notes
        -----
        **Lazy implementations**

        The Python language requires the return value to be of type ``int``. Lazy implementations are therefore not able to return any kind of lazy/delayed object here and should raise a ``ValueError`` instead.

        .. versionchanged:: 2023.12
            Allowed lazy implementations to error.

        """
        ...

    def __int__(self, /) -> int:
        """
        Converts a zero-dimensional array to a Python ``int`` object.

        Parameters
        ----------
        self
            zero-dimensional array instance. Should have a real-valued or boolean data type. If ``self`` has a complex floating-point data type, the function must raise a ``TypeError``.

        Returns
        -------
        out: int
            a Python ``int`` object representing the single element of the array instance.

        Notes
        -----
        **Special cases**

        For boolean operands,

        - If ``self`` is ``True``, the result is ``1``.
        - If ``self`` is ``False``, the result is ``0``.

        For floating-point operands,

        - If ``self`` is a finite number, the result is the integer part of ``self``.
        - If ``self`` is ``-0``, the result is ``0``.

        **Raises**

        For floating-point operands,

        - If ``self`` is either ``+infinity`` or ``-infinity``, raise ``OverflowError``.
        - If ``self`` is ``NaN``, raise ``ValueError``.

        Notes
        -----
        **Lazy implementations**

        The Python language requires the return value to be of type ``int``. Lazy implementations are therefore not able to return any kind of lazy/delayed object here and should raise a ``ValueError`` instead.

        .. versionchanged:: 2022.12
            Added boolean and complex data type support.

        .. versionchanged:: 2023.12
            Allowed lazy implementations to error.

        """
        ...

    def __invert__(self, /) -> Self:
        """
        Evaluates ``~self_i`` for each element of an array instance.

        Parameters
        ----------
        self
            array instance. Should have an integer or boolean data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have the same data type as `self`.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.bitwise_invert`.

        """
        ...

    def __le__(self, other: int | float | Self, /) -> Self:
        """
        Computes the truth value of ``self_i <= other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

        Parameters
        ----------
        self
            array instance. Should have a real-valued data type.
        other: Union[int, float, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a real-valued data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type of ``bool``.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.less_equal`.

        """
        ...

    def __lshift__(self, other: int | Self, /) -> Self:
        """
        Evaluates ``self_i << other_i`` for each element of an array instance with the respective element  of the array ``other``.

        Parameters
        ----------
        self
            array instance. Should have an integer data type.
        other: Union[int, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have an integer data type. Each element must be greater than or equal to ``0``.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have the same data type as ``self``.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.bitwise_left_shift`.

        """
        ...

    def __lt__(self, other: int | float | Self, /) -> Self:
        """
        Computes the truth value of ``self_i < other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

        Parameters
        ----------
        self
            array instance. Should have a real-valued data type.
        other: Union[int, float, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a real-valued data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type of ``bool``.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.less`.

        """
        ...

    def __matmul__(self, other: Self, /) -> Self:
        """
        Computes the matrix product.

        .. note::
           The ``matmul`` function must implement the same semantics as the built-in ``@`` operator (see `PEP 465 <https://www.python.org/dev/peps/pep-0465>`_).

        Parameters
        ----------
        self
            array instance. Should have a numeric data type. Must have at least one dimension. If ``self`` is one-dimensional having shape ``(M,)`` and ``other`` has more than one dimension, ``self`` must be promoted to a two-dimensional array by prepending ``1`` to its dimensions (i.e., must have shape ``(1, M)``). After matrix multiplication, the prepended dimensions in the returned array must be removed. If ``self`` has more than one dimension (including after vector-to-matrix promotion), ``shape(self)[:-2]`` must be compatible with ``shape(other)[:-2]`` (after vector-to-matrix promotion) (see :ref:`broadcasting`). If ``self`` has shape ``(..., M, K)``, the innermost two dimensions form matrices on which to perform matrix multiplication.
        other: array
            other array. Should have a numeric data type. Must have at least one dimension. If ``other`` is one-dimensional having shape ``(N,)`` and ``self`` has more than one dimension, ``other`` must be promoted to a two-dimensional array by appending ``1`` to its dimensions (i.e., must have shape ``(N, 1)``). After matrix multiplication, the appended dimensions in the returned array must be removed. If ``other`` has more than one dimension (including after vector-to-matrix promotion), ``shape(other)[:-2]`` must be compatible with ``shape(self)[:-2]`` (after vector-to-matrix promotion) (see :ref:`broadcasting`). If ``other`` has shape ``(..., K, N)``, the innermost two dimensions form matrices on which to perform matrix multiplication.


        .. note::
           If either ``x1`` or ``x2`` has a complex floating-point data type, neither argument must be complex-conjugated or transposed. If conjugation and/or transposition is desired, these operations should be explicitly performed prior to computing the matrix product.

        Returns
        -------
        out: array
            -   if both ``self`` and ``other`` are one-dimensional arrays having shape ``(N,)``, a zero-dimensional array containing the inner product as its only element.
            -   if ``self`` is a two-dimensional array having shape ``(M, K)`` and ``other`` is a two-dimensional array having shape ``(K, N)``, a two-dimensional array containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ and having shape ``(M, N)``.
            -   if ``self`` is a one-dimensional array having shape ``(K,)`` and ``other`` is an array having shape ``(..., K, N)``, an array having shape ``(..., N)`` (i.e., prepended dimensions during vector-to-matrix promotion must be removed) and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_.
            -   if ``self`` is an array having shape ``(..., M, K)`` and ``other`` is a one-dimensional array having shape ``(K,)``, an array having shape ``(..., M)`` (i.e., appended dimensions during vector-to-matrix promotion must be removed) and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_.
            -   if ``self`` is a two-dimensional array having shape ``(M, K)`` and ``other`` is an array having shape ``(..., K, N)``, an array having shape ``(..., M, N)`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.
            -   if ``self`` is an array having shape ``(..., M, K)`` and ``other`` is a two-dimensional array having shape ``(K, N)``, an array having shape ``(..., M, N)`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.
            -   if either ``self`` or ``other`` has more than two dimensions, an array having a shape determined by :ref:`broadcasting` ``shape(self)[:-2]`` against ``shape(other)[:-2]`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.
            -   The returned array must have a data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Results must equal the results returned by the equivalent function :func:`~array_api.matmul`.

        **Raises**

        - if either ``self`` or ``other`` is a zero-dimensional array.
        - if ``self`` is a one-dimensional array having shape ``(K,)``, ``other`` is a one-dimensional array having shape ``(L,)``, and ``K != L``.
        - if ``self`` is a one-dimensional array having shape ``(K,)``, ``other`` is an array having shape ``(..., L, N)``, and ``K != L``.
        - if ``self`` is an array having shape ``(..., M, K)``, ``other`` is a one-dimensional array having shape ``(L,)``, and ``K != L``.
        - if ``self`` is an array having shape ``(..., M, K)``, ``other`` is an array having shape ``(..., L, N)``, and ``K != L``.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __mod__(self, other: int | float | Self, /) -> Self:
        """
        Evaluates ``self_i % other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           For input arrays which promote to an integer data type, the result of division by zero is unspecified and thus implementation-defined.

        Parameters
        ----------
        self
            array instance. Should have a real-valued data type.
        other: Union[int, float, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a real-valued data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. Each element-wise result must have the same sign as the respective element ``other_i``. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.


        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.remainder`.

        """
        ...

    def __mul__(self, other: int | float | complex | Self, /) -> Self:
        """
        Calculates the product for each element of an array instance with the respective element of the array ``other``.

        .. note::
           Floating-point multiplication is not always associative due to finite precision.

        Parameters
        ----------
        self
            array instance. Should have a numeric data type.
        other: Union[int, float, complex, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the element-wise products. The returned array must have a data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.multiply`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __ne__(self, other: int | float | complex | bool | Self, /) -> Self:  # type: ignore[override]
        """
        Computes the truth value of ``self_i != other_i`` for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance. May have any data type.
        other: Union[int, float, complex, bool, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). May have any data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type of ``bool`` (i.e., must be a boolean array).


        Notes
        -----

        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.not_equal`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __neg__(self, /) -> Self:
        """
        Evaluates ``-self_i`` for each element of an array instance.

        .. note::
           For signed integer data types, the numerical negative of the minimum representable integer is implementation-dependent.

        .. note::
           If ``self`` has a complex floating-point data type, both the real and imaginary components for each ``self_i`` must be negated (a result which follows from the rules of complex number multiplication).

        Parameters
        ----------
        self
            array instance. Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the evaluated result for each element in ``self``. The returned array must have a data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.negative`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __or__(self, other: int | bool | Self, /) -> Self:
        """
        Evaluates ``self_i | other_i`` for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance. Should have an integer or boolean data type.
        other: Union[int, bool, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have an integer or boolean data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.bitwise_or`.

        """
        ...

    def __pos__(self, /) -> Self:
        """
        Evaluates ``+self_i`` for each element of an array instance.

        Parameters
        ----------
        self
            array instance. Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the evaluated result for each element. The returned array must have the same data type as ``self``.

        Notes
        -----

        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.positive`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __pow__(self, other: int | float | complex | Self, /) -> Self:
        """
        Calculates an implementation-dependent approximation of exponentiation by raising each element (the base) of an array instance to the power of ``other_i`` (the exponent), where ``other_i`` is the corresponding element of the array ``other``.

        .. note::
           If both ``self`` and ``other`` have integer data types, the result of ``__pow__`` when `other_i` is negative (i.e., less than zero) is unspecified and thus implementation-dependent.

           If ``self`` has an integer data type and ``other`` has a floating-point data type, behavior is implementation-dependent, as type promotion between data type "kinds" (e.g., integer versus floating-point) is unspecified.

        Parameters
        ----------
        self
            array instance whose elements correspond to the exponentiation base. Should have a numeric data type.
        other: Union[int, float, complex, array]
            other array whose elements correspond to the exponentiation exponent. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.pow`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __rshift__(self, other: int | Self, /) -> Self:
        """
        Evaluates ``self_i >> other_i`` for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance. Should have an integer data type.
        other: Union[int, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have an integer data type. Each element must be greater than or equal to ``0``.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have the same data type as ``self``.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.bitwise_right_shift`.

        """
        ...

    def __setitem__(self, key: int | slice | ellipsis | tuple[int | slice | ellipsis, ...] | Self, value: int | float | complex | bool | Self, /) -> None:
        """
        Sets ``self[key]`` to ``value``.

        See :ref:`indexing` for details on supported indexing semantics.

        Parameters
        ----------
        self
            array instance.
        key: Union[int, slice, ellipsis, Tuple[Union[int, slice, ellipsis], ...], array]
            index key.
        value: Union[int, float, complex, bool, array]
            value(s) to set. Must be compatible with ``self[key]`` (see :ref:`broadcasting`).


        .. note::

           Setting array values must not affect the data type of ``self``.

           When ``value`` is a Python scalar (i.e., ``int``, ``float``, ``bool``), behavior must follow specification guidance on mixing arrays with Python scalars (see :ref:`type-promotion`).

           When ``value`` is an ``array`` of a different data type than ``self``, how values are cast to the data type of ``self`` is implementation defined.

        """
        ...

    def __sub__(self, other: int | float | complex | Self, /) -> Self:
        """
        Calculates the difference for each element of an array instance with the respective element of the array ``other``.

        The result of ``self_i - other_i`` must be the same as ``self_i + (-other_i)`` and must be governed by the same floating-point rules as addition (see :meth:`array.__add__`).

        Parameters
        ----------
        self
            array instance (minuend array). Should have a numeric data type.
        other: Union[int, float, complex, array]
            subtrahend array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the element-wise differences. The returned array must have a data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.subtract`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __truediv__(self, other: int | float | complex | Self, /) -> Self:
        """
        Evaluates ``self_i / other_i`` for each element of an array instance with the respective element of the array ``other``.

        .. note::
           If one or both of ``self`` and ``other`` have integer data types, the result is implementation-dependent, as type promotion between data type "kinds" (e.g., integer versus floating-point) is unspecified.

           Specification-compliant libraries may choose to raise an error or return an array containing the element-wise results. If an array is returned, the array must have a real-valued floating-point data type.

        Parameters
        ----------
        self
            array instance. Should have a numeric data type.
        other: Union[int, float, complex, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array should have a floating-point data type determined by :ref:`type-promotion`.

        Notes
        -----

        .. note::
           Element-wise results, including special cases, must equal the results returned by the equivalent element-wise function :func:`~array_api.divide`.

        .. versionchanged:: 2022.12
            Added complex data type support.

        """
        ...

    def __xor__(self, other: int | bool | Self, /) -> Self:
        """
        Evaluates ``self_i ^ other_i`` for each element of an array instance with the respective element of the array ``other``.

        Parameters
        ----------
        self
            array instance. Should have an integer or boolean data type.
        other: Union[int, bool, array]
            other array. Must be compatible with ``self`` (see :ref:`broadcasting`). Should have an integer or boolean data type.

        Returns
        -------
        out: array
            an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.


        .. note::
           Element-wise results must equal the results returned by the equivalent element-wise function :func:`~array_api.bitwise_xor`.

        """
        ...

    def to_device(self, device: TDevice, /, *, stream: int | Any | None = None) -> Self:
        """
        Copy the array from the device on which it currently resides to the specified ``device``.

        Parameters
        ----------
        self
            array instance.
        device: device
            a ``device`` object (see :ref:`device-support`).
        stream: Optional[Union[int, Any]]
            stream object to use during copy. In addition to the types supported in :meth:`array.__dlpack__`, implementations may choose to support any library-specific stream object with the caveat that any code using such an object would not be portable.

        Returns
        -------
        out: array
            an array with the same data and data type as ``self`` and located on the specified ``device``.


        Notes
        -----
        -   When a provided ``device`` object corresponds to the same device on which an array instance resides, implementations may choose to perform an explicit copy or return ``self``.
        -   If ``stream`` is provided, the copy operation should be enqueued on the provided ``stream``; otherwise, the copy operation should be enqueued on the default stream/queue. Whether the copy is performed synchronously or asynchronously is implementation-dependent. Accordingly, if synchronization is required to guarantee data safety, this must be clearly explained in a conforming array library's documentation.

        .. versionchanged:: 2023.12
           Clarified behavior when a provided ``device`` object corresponds to the device on which an array instance resides.

        """
        ...


@runtime_checkable
class astype[TArray: Array, TDtype, TDevice](Protocol):
    """
    Copies an array to a specified data type irrespective of :ref:`type-promotion` rules.

    .. note::
       Casting floating-point ``NaN`` and ``infinity`` values to integral data types is not specified and is implementation-dependent.

    .. note::
       Casting a complex floating-point array to a real-valued data type should not be permitted.

       Historically, when casting a complex floating-point array to a real-valued data type, libraries such as NumPy have discarded imaginary components such that, for a complex floating-point array ``x``, ``astype(x)`` equals ``astype(real(x))``). This behavior is considered problematic as the choice to discard the imaginary component is arbitrary and introduces more than one way to achieve the same outcome (i.e., for a complex floating-point array ``x``, ``astype(x)`` and ``astype(real(x))`` versus only ``astype(imag(x))``). Instead, in order to avoid ambiguity and to promote clarity, this specification requires that array API consumers explicitly express which component should be cast to a specified real-valued data type.

    .. note::
       When casting a boolean input array to a real-valued data type, a value of ``True`` must cast to a real-valued number equal to ``1``, and a value of ``False`` must cast to a real-valued number equal to ``0``.

       When casting a boolean input array to a complex floating-point data type, a value of ``True`` must cast to a complex number equal to ``1 + 0j``, and a value of ``False`` must cast to a complex number equal to ``0 + 0j``.

    .. note::
       When casting a real-valued input array to ``bool``, a value of ``0`` must cast to ``False``, and a non-zero value must cast to ``True``.

       When casting a complex floating-point array to ``bool``, a value of ``0 + 0j`` must cast to ``False``, and all other values must cast to ``True``.

    Parameters
    ----------
    x: array
        array to cast.
    dtype: dtype
        desired data type.
    copy: bool
        specifies whether to copy an array when the specified ``dtype`` matches the data type of the input array ``x``. If ``True``, a newly allocated array must always be returned. If ``False`` and the specified ``dtype`` matches the data type of the input array, the input array must be returned; otherwise, a newly allocated array must be returned. Default: ``True``.
    device: Optional[device]
        device on which to place the returned array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.

    Returns
    -------
    out: array
        an array having the specified data type. The returned array must have the same shape as ``x``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Added device keyword argument support.

    """

    @abstractmethod
    def __call__(self, x: TArray, dtype: TDtype, /, *, copy: bool = True, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class can_cast[TArray: Array, TDtype](Protocol):
    """
    Determines if one data type can be cast to another data type according :ref:`type-promotion` rules.

    Parameters
    ----------
    from_: Union[dtype, array]
        input data type or array from which to cast.
    to: dtype
        desired data type.

    Returns
    -------
    out: bool
        ``True`` if the cast can occur according to :ref:`type-promotion` rules; otherwise, ``False``.

    """

    @abstractmethod
    def __call__(self, from_: TDtype | TArray, to: TDtype, /) -> bool: ...


@runtime_checkable
class finfo[TArray: Array, TDtype](Protocol):
    """
    Machine limits for floating-point data types.

    Parameters
    ----------
    type: Union[dtype, array]
        the kind of floating-point data-type about which to get information. If complex, the information is about its component data type.

        .. note::
           Complex floating-point data types are specified to always use the same precision for both its real and imaginary components, so the information should be true for either component.

    Returns
    -------
    out: finfo object
        an object having the following attributes:

        - **bits**: *int*

          number of bits occupied by the real-valued floating-point data type.

        - **eps**: *float*

          difference between 1.0 and the next smallest representable real-valued floating-point number larger than 1.0 according to the IEEE-754 standard.

        - **max**: *float*

          largest representable real-valued number.

        - **min**: *float*

          smallest representable real-valued number.

        - **smallest_normal**: *float*

          smallest positive real-valued floating-point number with full precision.

        - **dtype**: dtype

          real-valued floating-point data type.

          .. versionadded:: 2022.12

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, type: TDtype | TArray, /) -> finfo_object: ...


@runtime_checkable
class iinfo[TArray: Array, TDtype](Protocol):
    """
    Machine limits for integer data types.

    Parameters
    ----------
    type: Union[dtype, array]
        the kind of integer data-type about which to get information.

    Returns
    -------
    out: iinfo object
        an object having the following attributes:

        - **bits**: *int*

          number of bits occupied by the type.

        - **max**: *int*

          largest representable number.

        - **min**: *int*

          smallest representable number.

        - **dtype**: dtype

          integer data type.

          .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, type: TDtype | TArray, /) -> iinfo_object: ...


@runtime_checkable
class isdtype[TDtype](Protocol):
    """
    Returns a boolean indicating whether a provided dtype is of a specified data type "kind".

    Parameters
    ----------
    dtype: dtype
        the input dtype.
    kind: Union[str, dtype, Tuple[Union[str, dtype], ...]]
        data type kind.

        -   If ``kind`` is a dtype, the function must return a boolean indicating whether the input ``dtype`` is equal to the dtype specified by ``kind``.
        -   If ``kind`` is a string, the function must return a boolean indicating whether the input ``dtype`` is of a specified data type kind. The following dtype kinds must be supported:

            -   ``'bool'``: boolean data types (e.g., ``bool``).
            -   ``'signed integer'``: signed integer data types (e.g., ``int8``, ``int16``, ``int32``, ``int64``).
            -   ``'unsigned integer'``: unsigned integer data types (e.g., ``uint8``, ``uint16``, ``uint32``, ``uint64``).
            -   ``'integral'``: integer data types. Shorthand for ``('signed integer', 'unsigned integer')``.
            -   ``'real floating'``: real-valued floating-point data types (e.g., ``float32``, ``float64``).
            -   ``'complex floating'``: complex floating-point data types (e.g., ``complex64``, ``complex128``).
            -   ``'numeric'``: numeric data types. Shorthand for ``('integral', 'real floating', 'complex floating')``.

        -   If ``kind`` is a tuple, the tuple specifies a union of dtypes and/or kinds, and the function must return a boolean indicating whether the input ``dtype`` is either equal to a specified dtype or belongs to at least one specified data type kind.

        .. note::
           A conforming implementation of the array API standard is **not** limited to only including the dtypes described in this specification in the required data type kinds. For example, implementations supporting ``float16`` and ``bfloat16`` can include ``float16`` and ``bfloat16`` in the ``real floating`` data type kind. Similarly, implementations supporting ``int128`` can include ``int128`` in the ``signed integer`` data type kind.

           In short, conforming implementations may extend data type kinds; however, data type kinds must remain consistent (e.g., only integer dtypes may belong to integer data type kinds and only floating-point dtypes may belong to floating-point data type kinds), and extensions must be clearly documented as such in library documentation.

    Returns
    -------
    out: bool
        boolean indicating whether a provided dtype is of a specified data type kind.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, /, dtype: TDtype, kind: TDtype | str | tuple[TDtype | str, ...]) -> bool: ...


@runtime_checkable
class result_type[TArray: Array, TDtype](Protocol):
    """
    Returns the dtype that results from applying the type promotion rules (see :ref:`type-promotion`) to the arguments.

    .. note::
       If provided mixed dtypes (e.g., integer and floating-point), the returned dtype will be implementation-specific.

    Parameters
    ----------
    arrays_and_dtypes: Union[array, dtype]
        an arbitrary number of input arrays and/or dtypes.

    Returns
    -------
    out: dtype
        the dtype resulting from an operation involving the input arrays and dtypes.

    """

    @abstractmethod
    def __call__(self, /, *arrays_and_dtypes: TArray | TDtype) -> TDtype: ...


@runtime_checkable
class cumulative_sum[TArray: Array, TDtype](Protocol):
    """
    Calculates the cumulative sum of elements in the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.
    axis: Optional[int]
        axis along which a cumulative sum must be computed. If ``axis`` is negative, the function must determine the axis along which to compute a cumulative sum by counting from the last dimension.

        If ``x`` is a one-dimensional array, providing an ``axis`` is optional; however, if ``x`` has more than one dimension, providing an ``axis`` is required.

    dtype: Optional[dtype]
        data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:

        -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.
        -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).

        If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.

    include_initial: bool
        boolean indicating whether to include the initial value as the first value in the output. By convention, the initial value must be the additive identity (i.e., zero). Default: ``False``.

    Returns
    -------
    out: array
        an array containing the cumulative sums. The returned array must have a data type as described by the ``dtype`` parameter above.

        Let ``N`` be the size of the axis along which to compute the cumulative sum. The returned array must have a shape determined according to the following rules:

        -   if ``include_initial`` is ``True``, the returned array must have the same shape as ``x``, except the size of the axis along which to compute the cumulative sum must be ``N+1``.
        -   if ``include_initial`` is ``False``, the returned array must have the same shape as ``x``.

    Notes
    -----
    **Special Cases**

    For both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.add`.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | None = None, dtype: TDtype | None = None, include_initial: bool = False) -> TArray: ...


@runtime_checkable
class max[TArray: Array](Protocol):
    """
    Calculates the maximum value of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which maximum values must be computed. By default, the maximum value must be computed over the entire array. If a tuple of integers, maximum values must be computed over multiple axes. Default: ``None``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the maximum value was computed over the entire array, a zero-dimensional array containing the maximum value; otherwise, a non-zero-dimensional array containing the maximum values. The returned array must have the same data type as ``x``.

    Notes
    -----
    When the number of elements over which to compute the maximum value is zero, the maximum value is implementation-defined. Specification-compliant libraries may choose to raise an error, return a sentinel value (e.g., if ``x`` is a floating-point input array, return ``NaN``), or return the minimum possible value for the input array ``x`` data type (e.g., if ``x`` is a floating-point array, return ``-infinity``).

    The order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a maximum value, specification-compliant libraries may choose to return either value.

    For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).

    **Special Cases**

    For floating-point operands,

    -   If ``x_i`` is ``NaN``, the maximum value is ``NaN`` (i.e., ``NaN`` values propagate).

    .. versionchanged:: 2023.12
       Clarified that the order of signed zeros is implementation-defined.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class mean[TArray: Array](Protocol):
    """
    Calculates the arithmetic mean of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued floating-point data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which arithmetic means must be computed. By default, the mean must be computed over the entire array. If a tuple of integers, arithmetic means must be computed over multiple axes. Default: ``None``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the arithmetic mean was computed over the entire array, a zero-dimensional array containing the arithmetic mean; otherwise, a non-zero-dimensional array containing the arithmetic means. The returned array must have the same data type as ``x``.

        .. note::
           While this specification recommends that this function only accept input arrays having a real-valued floating-point data type, specification-compliant array libraries may choose to accept input arrays having an integer data type. While mixed data type promotion is implementation-defined, if the input array ``x`` has an integer data type, the returned array must have the default real-valued floating-point data type.

    Notes
    -----
    **Special Cases**

    Let ``N`` equal the number of elements over which to compute the arithmetic mean.

    -   If ``N`` is ``0``, the arithmetic mean is ``NaN``.
    -   If ``x_i`` is ``NaN``, the arithmetic mean is ``NaN`` (i.e., ``NaN`` values propagate).

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class min[TArray: Array](Protocol):
    """
    Calculates the minimum value of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which minimum values must be computed. By default, the minimum value must be computed over the entire array. If a tuple of integers, minimum values must be computed over multiple axes. Default: ``None``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the minimum value was computed over the entire array, a zero-dimensional array containing the minimum value; otherwise, a non-zero-dimensional array containing the minimum values. The returned array must have the same data type as ``x``.

    Notes
    -----
    When the number of elements over which to compute the minimum value is zero, the minimum value is implementation-defined. Specification-compliant libraries may choose to raise an error, return a sentinel value (e.g., if ``x`` is a floating-point input array, return ``NaN``), or return the maximum possible value for the input array ``x`` data type (e.g., if ``x`` is a floating-point array, return ``+infinity``).

    The order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a minimum value, specification-compliant libraries may choose to return either value.

    For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).

    **Special Cases**

    For floating-point operands,

    -   If ``x_i`` is ``NaN``, the minimum value is ``NaN`` (i.e., ``NaN`` values propagate).

    .. versionchanged:: 2023.12
       Clarified that the order of signed zeros is implementation-defined.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class prod[TArray: Array, TDtype](Protocol):
    """
    Calculates the product of input array ``x`` elements.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which products must be computed. By default, the product must be computed over the entire array. If a tuple of integers, products must be computed over multiple axes. Default: ``None``.

    dtype: Optional[dtype]
        data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:

        -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.
        -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).

        If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.

    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the product was computed over the entire array, a zero-dimensional array containing the product; otherwise, a non-zero-dimensional array containing the products. The returned array must have a data type as described by the ``dtype`` parameter above.

    Notes
    -----
    **Special Cases**

    Let ``N`` equal the number of elements over which to compute the product.

    -   If ``N`` is ``0``, the product is `1` (i.e., the empty product).

    For both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.multiply`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Required the function to return a floating-point array having the same data type as the input array when provided a floating-point array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, dtype: TDtype | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class std[TArray: Array](Protocol):
    """
    Calculates the standard deviation of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued floating-point data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which standard deviations must be computed. By default, the standard deviation must be computed over the entire array. If a tuple of integers, standard deviations must be computed over multiple axes. Default: ``None``.
    correction: Union[int, float]
        degrees of freedom adjustment. Setting this parameter to a value other than ``0`` has the effect of adjusting the divisor during the calculation of the standard deviation according to ``N-c`` where ``N`` corresponds to the total number of elements over which the standard deviation is computed and ``c`` corresponds to the provided degrees of freedom adjustment. When computing the standard deviation of a population, setting this parameter to ``0`` is the standard choice (i.e., the provided array contains data constituting an entire population). When computing the corrected sample standard deviation, setting this parameter to ``1`` is the standard choice (i.e., the provided array contains data sampled from a larger population; this is commonly referred to as Bessel's correction). Default: ``0``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the standard deviation was computed over the entire array, a zero-dimensional array containing the standard deviation; otherwise, a non-zero-dimensional array containing the standard deviations. The returned array must have the same data type as ``x``.

        .. note::
           While this specification recommends that this function only accept input arrays having a real-valued floating-point data type, specification-compliant array libraries may choose to accept input arrays having an integer data type. While mixed data type promotion is implementation-defined, if the input array ``x`` has an integer data type, the returned array must have the default real-valued floating-point data type.

    Notes
    -----
    **Special Cases**

    Let ``N`` equal the number of elements over which to compute the standard deviation.

    -   If ``N - correction`` is less than or equal to ``0``, the standard deviation is ``NaN``.
    -   If ``x_i`` is ``NaN``, the standard deviation is ``NaN`` (i.e., ``NaN`` values propagate).

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, correction: int | float = 0.0, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class sum[TArray: Array, TDtype](Protocol):
    """
    Calculates the sum of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which sums must be computed. By default, the sum must be computed over the entire array. If a tuple of integers, sums must be computed over multiple axes. Default: ``None``.

    dtype: Optional[dtype]
        data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:

        -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.
        -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).

        If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.

    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the sum was computed over the entire array, a zero-dimensional array containing the sum; otherwise, an array containing the sums. The returned array must have a data type as described by the ``dtype`` parameter above.

    Notes
    -----
    **Special Cases**

    Let ``N`` equal the number of elements over which to compute the sum.

    -   If ``N`` is ``0``, the sum is ``0`` (i.e., the empty sum).

    For both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.add`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Required the function to return a floating-point array having the same data type as the input array when provided a floating-point array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, dtype: TDtype | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class var[TArray: Array](Protocol):
    """
    Calculates the variance of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued floating-point data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which variances must be computed. By default, the variance must be computed over the entire array. If a tuple of integers, variances must be computed over multiple axes. Default: ``None``.
    correction: Union[int, float]
        degrees of freedom adjustment. Setting this parameter to a value other than ``0`` has the effect of adjusting the divisor during the calculation of the variance according to ``N-c`` where ``N`` corresponds to the total number of elements over which the variance is computed and ``c`` corresponds to the provided degrees of freedom adjustment. When computing the variance of a population, setting this parameter to ``0`` is the standard choice (i.e., the provided array contains data constituting an entire population). When computing the unbiased sample variance, setting this parameter to ``1`` is the standard choice (i.e., the provided array contains data sampled from a larger population; this is commonly referred to as Bessel's correction). Default: ``0``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if the variance was computed over the entire array, a zero-dimensional array containing the variance; otherwise, a non-zero-dimensional array containing the variances. The returned array must have the same data type as ``x``.


    .. note::
       While this specification recommends that this function only accept input arrays having a real-valued floating-point data type, specification-compliant array libraries may choose to accept input arrays having an integer data type. While mixed data type promotion is implementation-defined, if the input array ``x`` has an integer data type, the returned array must have the default real-valued floating-point data type.

    Notes
    -----
    **Special Cases**

    Let ``N`` equal the number of elements over which to compute the variance.

    -   If ``N - correction`` is less than or equal to ``0``, the variance is ``NaN``.
    -   If ``x_i`` is ``NaN``, the variance is ``NaN`` (i.e., ``NaN`` values propagate).

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, correction: int | float = 0.0, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class arange[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns evenly spaced values within the half-open interval ``[start, stop)`` as a one-dimensional array.

    Parameters
    ----------
    start: Union[int, float]
        if ``stop`` is specified, the start of interval (inclusive); otherwise, the end of the interval (exclusive). If ``stop`` is not specified, the default starting value is ``0``.
    stop: Optional[Union[int, float]]
        the end of the interval. Default: ``None``.
    step: Union[int, float]
        the distance between two adjacent elements (``out[i+1] - out[i]``). Must not be ``0``; may be negative, this results in an empty array if ``stop >= start``. Default: ``1``.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``start``, ``stop`` and ``step``. If those are all integers, the output array dtype must be the default integer dtype; if one or more have type ``float``, then the output array dtype must be the default real-valued floating-point data type. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.


    .. note::
       This function cannot guarantee that the interval does not include the ``stop`` value in those cases where ``step`` is not an integer and floating-point rounding errors affect the length of the output array.

    Returns
    -------
    out: array
        a one-dimensional array containing evenly spaced values. The length of the output array must be ``ceil((stop-start)/step)`` if ``stop - start`` and ``step`` have the same sign, and length ``0`` otherwise.

    """

    @abstractmethod
    def __call__(self, start: int | float, /, stop: int | float | None = None, step: int | float = 1, *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class asarray[TArray: Array, TDtype, TDevice](Protocol):
    r"""
    Convert the input to an array.

    Parameters
    ----------
    obj: Union[array, bool, int, float, complex, NestedSequence[bool | int | float | complex], SupportsBufferProtocol]
        object to be converted to an array. May be a Python scalar, a (possibly nested) sequence of Python scalars, or an object supporting the Python buffer protocol.

        .. admonition:: Tip
           :class: important

           An object supporting the buffer protocol can be turned into a memoryview through ``memoryview(obj)``.

    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from the data type(s) in ``obj``. If all input values are Python scalars, then, in order of precedence,

        -   if all values are of type ``bool``, the output data type must be ``bool``.
        -   if all values are of type ``int`` or are a mixture of ``bool`` and ``int``, the output data type must be the default integer data type.
        -   if one or more values are ``complex`` numbers, the output data type must be the default complex floating-point data type.
        -   if one or more values are ``float``\\s, the output data type must be the default real-valued floating-point data type.

        Default: ``None``.

        .. admonition:: Note
           :class: note

           If ``dtype`` is not ``None``, then array conversions should obey :ref:`type-promotion` rules. Conversions not specified according to :ref:`type-promotion` rules may or may not be permitted by a conforming array library. To perform an explicit cast, use :func:`array_api.astype`.

        .. note::
           If an input value exceeds the precision of the resolved output array data type, behavior is left unspecified and, thus, implementation-defined.

    device: Optional[device]
        device on which to place the created array. If ``device`` is ``None`` and ``obj`` is an array, the output array device must be inferred from ``obj``. Default: ``None``.
    copy: Optional[bool]
        boolean indicating whether or not to copy the input. If ``True``, the function must always copy. If ``False``, the function must never copy for input which supports the buffer protocol and must raise a ``ValueError`` in case a copy would be necessary. If ``None``, the function must reuse existing memory buffer if possible and copy otherwise. Default: ``None``.

    Returns
    -------
    out: array
        an array containing the data from ``obj``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, obj: TArray | bool | int | float | complex | NestedSequence | SupportsBufferProtocol, /, *, dtype: TDtype | None = None, device: TDevice | None = None, copy: bool | None = None) -> TArray: ...


@runtime_checkable
class empty[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns an uninitialized array having a specified `shape`.

    Parameters
    ----------
    shape: Union[int, Tuple[int, ...]]
        output array shape.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array containing uninitialized data.

    """

    @abstractmethod
    def __call__(self, /, shape: int | tuple[int, ...], *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class empty_like[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns an uninitialized array with the same ``shape`` as an input array ``x``.

    Parameters
    ----------
    x: array
        input array from which to derive the output array shape.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.

    Returns
    -------
    out: array
        an array having the same shape as ``x`` and containing uninitialized data.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class eye[TArray: Array, TDtype, TDevice](Protocol):
    r"""
    Returns a two-dimensional array with ones on the ``k``\\th diagonal and zeros elsewhere.

    .. note::
       An output array having a complex floating-point data type must have the value ``1 + 0j`` along the ``k``\\th diagonal and ``0 + 0j`` elsewhere.

    Parameters
    ----------
    n_rows: int
        number of rows in the output array.
    n_cols: Optional[int]
        number of columns in the output array. If ``None``, the default number of columns in the output array is equal to ``n_rows``. Default: ``None``.
    k: int
        index of the diagonal. A positive value refers to an upper diagonal, a negative value to a lower diagonal, and ``0`` to the main diagonal. Default: ``0``.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array where all elements are equal to zero, except for the ``k``\\th diagonal, whose values are equal to one.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, n_rows: int, n_cols: int | None = None, /, *, k: int = 0, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class from_dlpack[TArray: Array, TDevice](Protocol):
    """
    Returns a new array containing the data from another (array) object with a ``__dlpack__`` method.

    Parameters
    ----------
    x: object
        input (array) object.
    device: Optional[device]
        device on which to place the created array. If ``device`` is ``None`` and ``x`` supports DLPack, the output array must be on the same device as ``x``. Default: ``None``.

        The v2023.12 standard only mandates that a compliant library should offer a way for ``from_dlpack`` to return an array
        whose underlying memory is accessible to the Python interpreter, when the corresponding ``device`` is provided. If the
        array library does not support such cases at all, the function must raise ``BufferError``. If a copy must be made to
        enable this support but ``copy`` is set to ``False``, the function must raise ``ValueError``.

        Other device kinds will be considered for standardization in a future version of this API standard.
    copy: Optional[bool]
        boolean indicating whether or not to copy the input. If ``True``, the function must always copy. If ``False``, the function must never copy, and raise ``BufferError`` in case a copy is deemed necessary (e.g.  if a cross-device data movement is requested, and it is not possible without a copy). If ``None``, the function must reuse the existing memory buffer if possible and copy otherwise. Default: ``None``.

    Returns
    -------
    out: array
        an array containing the data in ``x``.

        .. admonition:: Note
           :class: note

           The returned array may be either a copy or a view. See :ref:`data-interchange` for details.

    Raises
    ------
    BufferError
        The ``__dlpack__`` and ``__dlpack_device__`` methods on the input array
        may raise ``BufferError`` when the data cannot be exported as DLPack
        (e.g., incompatible dtype, strides, or device). It may also raise other errors
        when export fails for other reasons (e.g., not enough memory available
        to materialize the data). ``from_dlpack`` must propagate such
        exceptions.
    AttributeError
        If the ``__dlpack__`` and ``__dlpack_device__`` methods are not present
        on the input array. This may happen for libraries that are never able
        to export their data with DLPack.
    ValueError
        If data exchange is possible via an explicit copy but ``copy`` is set to ``False``.

    Notes
    -----
    See :meth:`array.__dlpack__` for implementation suggestions for `from_dlpack` in
    order to handle DLPack versioning correctly.

    A way to move data from two array libraries to the same device (assumed supported by both libraries) in
    a library-agnostic fashion is illustrated below:

    .. code:: python

        def func(x, y):
            xp_x = x.__array_namespace__()
            xp_y = y.__array_namespace__()

            # Other functions than `from_dlpack` only work if both arrays are from the same library. So if
            # `y` is from a different one than `x`, let's convert `y` into an array of the same type as `x`:
            if not xp_x == xp_y:
                y = xp_x.from_dlpack(y, copy=True, device=x.device)

            # From now on use `xp_x.xxxxx` functions, as both arrays are from the library `xp_x`
            ...


    .. versionchanged:: 2023.12
       Required exceptions to address unsupported use cases.

    .. versionchanged:: 2023.12
       Added device and copy support.

    """

    @abstractmethod
    def __call__(self, x: object, /, *, device: TDevice | None = None, copy: bool | None = None) -> TArray: ...


@runtime_checkable
class full[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns a new array having a specified ``shape`` and filled with ``fill_value``.

    Parameters
    ----------
    shape: Union[int, Tuple[int, ...]]
        output array shape.
    fill_value: Union[bool, int, float, complex]
        fill value.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``fill_value`` according to the following rules:

        - If the fill value is an ``int``, the output array data type must be the default integer data type.
        - If the fill value is a ``float``, the output array data type must be the default real-valued floating-point data type.
        - If the fill value is a ``complex`` number, the output array data type must be the default complex floating-point data type.
        - If the fill value is a ``bool``, the output array must have a boolean data type. Default: ``None``.

        .. note::
           If the ``fill_value`` exceeds the precision of the resolved default output array data type, behavior is left unspecified and, thus, implementation-defined.

    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array where every element is equal to ``fill_value``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, /, shape: int | tuple[int, ...], fill_value: bool | int | float | complex, *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class full_like[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns a new array filled with ``fill_value`` and having the same ``shape`` as an input array ``x``.

    Parameters
    ----------
    x: array
        input array from which to derive the output array shape.
    fill_value: Union[bool, int, float, complex]
        fill value.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.

        .. note::
           If the ``fill_value`` exceeds the precision of the resolved output array data type, behavior is unspecified and, thus, implementation-defined.

        .. note::
           If the ``fill_value`` has a data type which is not of the same data type kind (boolean, integer, or floating-point) as the resolved output array data type (see :ref:`type-promotion`), behavior is unspecified and, thus, implementation-defined.

    device: Optional[device]
        device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.

    Returns
    -------
    out: array
        an array having the same shape as ``x`` and where every element is equal to ``fill_value``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, fill_value: bool | int | float | complex, *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class linspace[TArray: Array, TDtype, TDevice](Protocol):
    r"""
    Returns evenly spaced numbers over a specified interval.

    Let :math:`N` be the number of generated values (which is either ``num`` or ``num+1`` depending on whether ``endpoint`` is ``True`` or ``False``, respectively). For real-valued output arrays, the spacing between values is given by

    .. math::
       \\Delta_{\\textrm{real}} = \\frac{\\textrm{stop} - \\textrm{start}}{N - 1}

    For complex output arrays, let ``a = real(start)``, ``b = imag(start)``, ``c = real(stop)``, and ``d = imag(stop)``. The spacing between complex values is given by

    .. math::
       \\Delta_{\\textrm{complex}} = \\frac{c-a}{N-1} + \\frac{d-b}{N-1} j

    Parameters
    ----------
    start: Union[int, float, complex]
        the start of the interval.
    stop: Union[int, float, complex]
        the end of the interval. If ``endpoint`` is ``False``, the function must generate a sequence of ``num+1`` evenly spaced numbers starting with ``start`` and ending with ``stop`` and exclude the ``stop`` from the returned array such that the returned array consists of evenly spaced numbers over the half-open interval ``[start, stop)``. If ``endpoint`` is ``True``, the output array must consist of evenly spaced numbers over the closed interval ``[start, stop]``. Default: ``True``.

        .. note::
           The step size changes when `endpoint` is `False`.

    num: int
        number of samples. Must be a nonnegative integer value.
    dtype: Optional[dtype]
        output array data type. Should be a floating-point data type. If ``dtype`` is ``None``,

        -   if either ``start`` or ``stop`` is a ``complex`` number, the output data type must be the default complex floating-point data type.
        -   if both ``start`` and ``stop`` are real-valued, the output data type must be the default real-valued floating-point data type.

        Default: ``None``.

        .. admonition:: Note
           :class: note

           If ``dtype`` is not ``None``, conversion of ``start`` and ``stop`` should obey :ref:`type-promotion` rules. Conversions not specified according to :ref:`type-promotion` rules may or may not be permitted by a conforming array library.

    device: Optional[device]
        device on which to place the created array. Default: ``None``.
    endpoint: bool
        boolean indicating whether to include ``stop`` in the interval. Default: ``True``.

    Returns
    -------
    out: array
        a one-dimensional array containing evenly spaced values.

    Notes
    -----

    .. note::
       While this specification recommends that this function only return arrays having a floating-point data type, specification-compliant array libraries may choose to support output arrays having an integer data type (e.g., due to backward compatibility concerns). However, function behavior when generating integer output arrays is unspecified and, thus, is implementation-defined. Accordingly, using this function to generate integer output arrays is not portable.

    .. note::
       As mixed data type promotion is implementation-defined, behavior when ``start`` or ``stop`` exceeds the maximum safe integer of an output floating-point data type is implementation-defined. An implementation may choose to overflow or raise an exception.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, start: int | float | complex, stop: int | float | complex, /, num: int, *, dtype: TDtype | None = None, device: TDevice | None = None, endpoint: bool = True) -> TArray: ...


@runtime_checkable
class meshgrid[TArray: Array](Protocol):
    """
    Returns coordinate matrices from coordinate vectors.

    Parameters
    ----------
    arrays: array
        an arbitrary number of one-dimensional arrays representing grid coordinates. Each array should have the same numeric data type.
    indexing:  Literal["xy", "ij"]
        Cartesian ``'xy'`` or matrix ``'ij'`` indexing of output. If provided zero or one one-dimensional vector(s) (i.e., the zero- and one-dimensional cases, respectively), the ``indexing`` keyword has no effect and should be ignored. Default: ``'xy'``.

    Returns
    -------
    out: List[array]
        list of N arrays, where ``N`` is the number of provided one-dimensional input arrays. Each returned array must have rank ``N``. For ``N`` one-dimensional arrays having lengths ``Ni = len(xi)``,

        - if matrix indexing ``ij``, then each returned array must have the shape ``(N1, N2, N3, ..., Nn)``.
        - if Cartesian indexing ``xy``, then each returned array must have shape ``(N2, N1, N3, ..., Nn)``.

        Accordingly, for the two-dimensional case with input one-dimensional arrays of length ``M`` and ``N``, if matrix indexing ``ij``, then each returned array must have shape ``(M, N)``, and, if Cartesian indexing ``xy``, then each returned array must have shape ``(N, M)``.

        Similarly, for the three-dimensional case with input one-dimensional arrays of length ``M``, ``N``, and ``P``, if matrix indexing ``ij``, then each returned array must have shape ``(M, N, P)``, and, if Cartesian indexing ``xy``, then each returned array must have shape ``(N, M, P)``.

        Each returned array should have the same data type as the input arrays.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, /, *arrays: TArray, indexing: Literal["xy", "ij"] = "xy") -> list[TArray]: ...


@runtime_checkable
class ones[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns a new array having a specified ``shape`` and filled with ones.

    .. note::
       An output array having a complex floating-point data type must contain complex numbers having a real component equal to one and an imaginary component equal to zero (i.e., ``1 + 0j``).

    Parameters
    ----------
    shape: Union[int, Tuple[int, ...]]
        output array shape.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array containing ones.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, /, shape: int | tuple[int, ...], *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class ones_like[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns a new array filled with ones and having the same ``shape`` as an input array ``x``.

    .. note::
       An output array having a complex floating-point data type must contain complex numbers having a real component equal to one and an imaginary component equal to zero (i.e., ``1 + 0j``).

    Parameters
    ----------
    x: array
        input array from which to derive the output array shape.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.

    Returns
    -------
    out: array
        an array having the same shape as ``x`` and filled with ones.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class tril[TArray: Array](Protocol):
    """
    Returns the lower triangular part of a matrix (or a stack of matrices) ``x``.

    .. note::
       The lower triangular part of the matrix is defined as the elements on and below the specified diagonal ``k``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.
    k: int
        diagonal above which to zero elements. If ``k = 0``, the diagonal is the main diagonal. If ``k < 0``, the diagonal is below the main diagonal. If ``k > 0``, the diagonal is above the main diagonal. Default: ``0``.

        .. note::
           The main diagonal is defined as the set of indices ``{(i, i)}`` for ``i`` on the interval ``[0, min(M, N) - 1]``.

    Returns
    -------
    out: array
        an array containing the lower triangular part(s). The returned array must have the same shape and data type as ``x``. All elements above the specified diagonal ``k`` must be zeroed. The returned array should be allocated on the same device as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, k: int = 0) -> TArray: ...


@runtime_checkable
class triu[TArray: Array](Protocol):
    """
    Returns the upper triangular part of a matrix (or a stack of matrices) ``x``.

    .. note::
       The upper triangular part of the matrix is defined as the elements on and above the specified diagonal ``k``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.
    k: int
        diagonal below which to zero elements. If ``k = 0``, the diagonal is the main diagonal. If ``k < 0``, the diagonal is below the main diagonal. If ``k > 0``, the diagonal is above the main diagonal. Default: ``0``.

        .. note::
           The main diagonal is defined as the set of indices ``{(i, i)}`` for ``i`` on the interval ``[0, min(M, N) - 1]``.

    Returns
    -------
    out: array
        an array containing the upper triangular part(s). The returned array must have the same shape and data type as ``x``. All elements below the specified diagonal ``k`` must be zeroed. The returned array should be allocated on the same device as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, k: int = 0) -> TArray: ...


@runtime_checkable
class zeros[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns a new array having a specified ``shape`` and filled with zeros.

    Parameters
    ----------
    shape: Union[int, Tuple[int, ...]]
        output array shape.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array containing zeros.

    """

    @abstractmethod
    def __call__(self, /, shape: int | tuple[int, ...], *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class zeros_like[TArray: Array, TDtype, TDevice](Protocol):
    """
    Returns a new array filled with zeros and having the same ``shape`` as an input array ``x``.

    Parameters
    ----------
    x: array
        input array from which to derive the output array shape.
    dtype: Optional[dtype]
        output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.
    device: Optional[device]
        device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.

    Returns
    -------
    out: array
        an array having the same shape as ``x`` and filled with zeros.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, dtype: TDtype | None = None, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class cholesky[TArray: Array](Protocol):
    r"""
    Returns the lower (upper) Cholesky decomposition of a complex Hermitian or real symmetric positive-definite matrix ``x``.

    If ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    The lower **Cholesky decomposition** of a complex Hermitian or real symmetric positive-definite matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as

    .. math::
       x = LL^{H} \\qquad \\text{L $\\in\\ \\mathbb{K}^{n \\times n}$}

    where :math:`L` is a lower triangular matrix and :math:`L^{H}` is the conjugate transpose when :math:`L` is complex-valued and the transpose when :math:`L` is real-valued.

    The upper Cholesky decomposition is defined similarly

    .. math::
       x = U^{H}U \\qquad \\text{U $\\in\\ \\mathbb{K}^{n \\times n}$}

    where :math:`U` is an upper triangular matrix.

    When ``x`` is a stack of matrices, the function must compute the Cholesky decomposition for each matrix in the stack.

    .. note::
       Whether an array library explicitly checks whether an input array is Hermitian or a symmetric positive-definite matrix (or a stack of matrices) is implementation-defined.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square complex Hermitian or real symmetric positive-definite matrices. Should have a floating-point data type.
    upper: bool
        If ``True``, the result must be the upper-triangular Cholesky factor :math:`U`. If ``False``, the result must be the lower-triangular Cholesky factor :math:`L`. Default: ``False``.

    Returns
    -------
    out: array
        an array containing the Cholesky factors for each square matrix. If ``upper`` is ``False``, the returned array must contain lower-triangular matrices; otherwise, the returned array must contain upper-triangular matrices. The returned array must have a floating-point data type determined by :ref:`type-promotion` and must have the same shape as ``x``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, upper: bool = False) -> TArray: ...


@runtime_checkable
class cross[TArray: Array](Protocol):
    """
    Returns the cross product of 3-element vectors.

    If ``x1`` and/or ``x2`` are multi-dimensional arrays (i.e., the broadcasted result has a rank greater than ``1``), then the cross-product of each pair of corresponding 3-element vectors is independently computed.

    Parameters
    ----------
    x1: array
        first input array. Must have a numeric data type. The size of the axis over which the cross product is to be computed must be equal to 3.
    x2: array
        second input array. Must be broadcast compatible with ``x1`` along all axes other than the axis along which the cross-product is computed (see :ref:`broadcasting`). The size of the axis over which the cross product is to be computed must be equal to 3. Must have a numeric data type.

        .. note::
           The compute axis (dimension) must not be broadcasted.

    axis: int
        the axis (dimension) of ``x1`` and ``x2`` containing the vectors for which to compute the cross product. Should be an integer on the interval ``[-N, -1]``, where ``N`` is ``min(x1.ndim, x2.ndim)``. The function must determine the axis along which to compute the cross product by counting backward from the last dimension (where ``-1`` refers to the last dimension). By default, the function must compute the cross product over the last axis. Default: ``-1``.

    Returns
    -------
    out: array
        an array containing the cross products. The returned array must have a data type determined by :ref:`type-promotion`.


    Notes
    -----
    **Raises**

    -   if the size of the axis over which to compute the cross product is not equal to ``3`` (before broadcasting) for both ``x1`` and ``x2``.

    .. versionchanged:: 2022.12
       Added support for broadcasting.

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Restricted broadcasting to only non-compute axes and required that ``axis`` be a negative integer.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /, *, axis: int = -1) -> TArray: ...


@runtime_checkable
class det[TArray: Array](Protocol):
    """
    Returns the determinant of a square matrix (or a stack of square matrices) ``x``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.

    Returns
    -------
    out: array
        if ``x`` is a two-dimensional array, a zero-dimensional array containing the determinant; otherwise, a non-zero dimensional array containing the determinant for each square matrix. The returned array must have the same data type as ``x``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class diagonal[TArray: Array](Protocol):
    """
    Returns the specified diagonals of a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.
    offset: int
        offset specifying the off-diagonal relative to the main diagonal.

        - ``offset = 0``: the main diagonal.
        - ``offset > 0``: off-diagonal above the main diagonal.
        - ``offset < 0``: off-diagonal below the main diagonal.

        Default: `0`.

    Returns
    -------
    out: array
        an array containing the diagonals and whose shape is determined by removing the last two dimensions and appending a dimension equal to the size of the resulting diagonals. The returned array must have the same data type as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, offset: int = 0) -> TArray: ...


@runtime_checkable
class eigh[TArray: Array](Protocol):
    r"""
    Returns an eigenvalue decomposition of a complex Hermitian or real symmetric matrix (or a stack of matrices) ``x``.

    If ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    The **eigenvalue decomposition** of a complex Hermitian or real symmetric matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as

    .. math::
       x = Q \\Lambda Q^H

    with :math:`Q \\in \\mathbb{K}^{n \\times n}` and :math:`\\Lambda \\in \\mathbb{R}^n` and where :math:`Q^H` is the conjugate transpose when :math:`Q` is complex and the transpose when :math:`Q` is real-valued and :math:`\\Lambda` is a diagonal matrix whose diagonal elements are the corresponding eigenvalues. When ``x`` is real-valued, :math:`Q` is orthogonal, and, when ``x`` is complex, :math:`Q` is unitary.

    .. note::
       The eigenvalues of a complex Hermitian or real symmetric matrix are always real.

    .. warning::
       The eigenvectors of a symmetric matrix are not unique and are not continuous with respect to ``x``. Because eigenvectors are not unique, different hardware and software may compute different eigenvectors.

       Non-uniqueness stems from the fact that multiplying an eigenvector by :math:`-1` when ``x`` is real-valued and by :math:`e^{\\phi j}` (:math:`\\phi \\in \\mathbb{R}`) when ``x`` is complex produces another set of valid eigenvectors.

    .. note::
       Whether an array library explicitly checks whether an input array is Hermitian or a symmetric matrix (or a stack of matrices) is implementation-defined.

    .. note::
       The function ``eig`` will be added in a future version of the specification.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.

    Returns
    -------
    out: Tuple[array, array]
        a namedtuple (``eigenvalues``, ``eigenvectors``) whose

        -   first element must have the field name ``eigenvalues`` (corresponding to :math:`\\operatorname{diag}\\Lambda` above) and must be an array consisting of computed eigenvalues. The array containing the eigenvalues must have shape ``(..., M)`` and must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then ``eigenvalues`` must be ``float64``).
        -   second element have have the field name ``eigenvectors`` (corresponding to :math:`Q` above) and must be an array where the columns of the inner most matrices contain the computed eigenvectors. These matrices must be orthogonal. The array containing the eigenvectors must have shape ``(..., M, M)`` and must have the same data type as ``x``.

    Notes
    -----

    .. note::
       Eigenvalue sort order is left unspecified and is thus implementation-dependent.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> tuple[TArray, TArray]: ...


@runtime_checkable
class eigvalsh[TArray: Array](Protocol):
    r"""
    Returns the eigenvalues of a complex Hermitian or real symmetric matrix (or a stack of matrices) ``x``.

    If ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    The **eigenvalues** of a complex Hermitian or real symmetric matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` are defined as the roots (counted with multiplicity) of the polynomial :math:`p` of degree :math:`n` given by

    .. math::
       p(\\lambda) = \\operatorname{det}(x - \\lambda I_n)

    where :math:`\\lambda \\in \\mathbb{R}` and where :math:`I_n` is the *n*-dimensional identity matrix.

    .. note:;
       The eigenvalues of a complex Hermitian or real symmetric matrix are always real.

    .. note::
       Whether an array library explicitly checks whether an input array is Hermitian or a symmetric matrix (or a stack of matrices) is implementation-defined.

    .. note::
       The function ``eigvals`` will be added in a future version of the specification.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the computed eigenvalues. The returned array must have shape ``(..., M)`` and have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then must have a ``float64`` data type).

    Notes
    -----

    .. note::
       Eigenvalue sort order is left unspecified and is thus implementation-dependent.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class inv[TArray: Array](Protocol):
    r"""
    Returns the multiplicative inverse of a square matrix (or a stack of square matrices) ``x``.

    If ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    The **inverse matrix** :math:`x^{-1} \\in\\ \\mathbb{K}^{n \\times n}` of a square matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as

    .. math::
       x^{-1}x = xx^{-1} = I_n

    where :math:`I_n` is the *n*-dimensional identity matrix.

    The inverse matrix exists if and only if ``x`` is invertible. When ``x`` is invertible, the inverse is unique.

    When ``x`` is a stack of matrices, the function must compute the inverse for each matrix in the stack.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the multiplicative inverses. The returned array must have a floating-point data type determined by :ref:`type-promotion` and must have the same shape as ``x``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class matrix_norm[TArray: Array](Protocol):
    """
    Computes the matrix norm of a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a floating-point data type.
    keepdims: bool
        If ``True``, the last two axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the last two axes (dimensions) must not be included in the result. Default: ``False``.
    ord: Optional[Union[int, float, Literal[inf, -inf, 'fro', 'nuc']]]
        order of the norm. The following mathematical norms must be supported:

        +------------------+---------------------------------+
        | ord              | description                     |
        +==================+=================================+
        | 'fro'            | Frobenius norm                  |
        +------------------+---------------------------------+
        | 'nuc'            | nuclear norm                    |
        +------------------+---------------------------------+
        | 1                | max(sum(abs(x), axis=0))        |
        +------------------+---------------------------------+
        | 2                | largest singular value          |
        +------------------+---------------------------------+
        | inf              | max(sum(abs(x), axis=1))        |
        +------------------+---------------------------------+

        The following non-mathematical "norms" must be supported:

        +------------------+---------------------------------+
        | ord              | description                     |
        +==================+=================================+
        | -1               | min(sum(abs(x), axis=0))        |
        +------------------+---------------------------------+
        | -2               | smallest singular value         |
        +------------------+---------------------------------+
        | -inf             | min(sum(abs(x), axis=1))        |
        +------------------+---------------------------------+

        If ``ord=1``, the norm corresponds to the induced matrix norm where ``p=1`` (i.e., the maximum absolute value column sum).

        If ``ord=2``, the norm corresponds to the induced matrix norm where ``p=inf`` (i.e., the maximum absolute value row sum).

        If ``ord=inf``, the norm corresponds to the induced matrix norm where ``p=2`` (i.e., the largest singular value).

        Default: ``'fro'``.

    Returns
    -------
    out: array
        an array containing the norms for each ``MxN`` matrix. If ``keepdims`` is ``False``, the returned array must have a rank which is two less than the rank of ``x``. If ``x`` has a real-valued data type, the returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`. If ``x`` has a complex-valued data type, the returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type).

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, keepdims: bool = False, ord: int | float | Literal[inf, -inf, "fro", "nuc"] | None = "fro") -> TArray:  # type: ignore[valid-type]
        ...


@runtime_checkable
class matrix_power[TArray: Array](Protocol):
    """
    Raises a square matrix (or a stack of square matrices) ``x`` to an integer power ``n``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.
    n: int
        integer exponent.

    Returns
    -------
    out: array
        if ``n`` is equal to zero, an array containing the identity matrix for each square matrix. If ``n`` is less than zero, an array containing the inverse of each square matrix raised to the absolute value of ``n``, provided that each square matrix is invertible. If ``n`` is greater than zero, an array containing the result of raising each square matrix to the power ``n``. The returned array must have the same shape as ``x`` and a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, n: int, /) -> TArray: ...


@runtime_checkable
class matrix_rank[TArray: Array](Protocol):
    """
    Returns the rank (i.e., number of non-zero singular values) of a matrix (or a stack of matrices).

    When ``x`` is a stack of matrices, the function must compute the number of non-zero singular values for each matrix in the stack.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a floating-point data type.
    rtol: Optional[Union[float, array]]
        relative tolerance for small singular values. Singular values approximately less than or equal to ``rtol * largest_singular_value`` are set to zero. If a ``float``, the value is equivalent to a zero-dimensional array having a real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``) and must be broadcast against each matrix. If an ``array``, must have a real-valued floating-point data type and must be compatible with ``shape(x)[:-2]`` (see :ref:`broadcasting`). If ``None``, the default value is ``max(M, N) * eps``, where ``eps`` must be the machine epsilon associated with the real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``). Default: ``None``.

    Returns
    -------
    out: array
        an array containing the ranks. The returned array must have the default integer data type and must have shape ``(...)`` (i.e., must have a shape equal to ``shape(x)[:-2]``).

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, rtol: float | TArray | None = None) -> TArray: ...


@runtime_checkable
class outer[TArray: Array](Protocol):
    """
    Returns the outer product of two vectors ``x1`` and ``x2``.

    Parameters
    ----------
    x1: array
        first one-dimensional input array of size ``N``. Must have a numeric data type.
    x2: array
        second one-dimensional input array of size ``M``. Must have a numeric data type.

    Returns
    -------
    out: array
        a two-dimensional array containing the outer product and whose shape is ``(N, M)``. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class pinv[TArray: Array](Protocol):
    r"""
    Returns the (Moore-Penrose) pseudo-inverse of a matrix (or a stack of matrices) ``x``.

    The pseudo-inverse of a matrix :math:`A`, denoted :math:`A^{+}`, is defined as the matrix that "solves" the least-squares problem :math:`Ax = b` (i.e., if :math:`\\overline{x}` is a solution, then :math:`A^{+}` is the matrix such that :math:`\\overline{x} = A^{+}b`).

    While the pseudo-inverse can be defined algebraically, one can understand the pseudo-inverse via singular value decomposition (SVD). Namely, if

    .. math::
       A = U \\Sigma V^H

    is a singular decomposition of :math:`A`, then

    .. math::
       A^{+} = U \\Sigma^{+} V^H

    where :math:`U` and :math:`V^H` are orthogonal matrices, :math:`\\Sigma` is a diagonal matrix consisting of :math:`A`'s singular values, and :math:`\\Sigma^{+}` is then a diagonal matrix consisting of the reciprocals of :math:`A`'s singular values, leaving zeros in place. During numerical computation, only elements larger than a small tolerance are considered nonzero, and all others replaced by zeros.

    When ``x`` is a stack of matrices, the function must compute the pseudo-inverse for each matrix in the stack.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a floating-point data type.
    rtol: Optional[Union[float, array]]
        relative tolerance for small singular values. Singular values approximately less than or equal to ``rtol * largest_singular_value`` are set to zero. If a ``float``, the value is equivalent to a zero-dimensional array having a real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``) and must be broadcast against each matrix. If an ``array``, must have a real-valued floating-point data type and must be compatible with ``shape(x)[:-2]`` (see :ref:`broadcasting`). If ``None``, the default value is ``max(M, N) * eps``, where ``eps`` must be the machine epsilon associated with the real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``). Default: ``None``.

    Returns
    -------
    out: array
        an array containing the pseudo-inverse(s). The returned array must have a floating-point data type determined by :ref:`type-promotion` and must have shape ``(..., N, M)`` (i.e., must have the same shape as ``x``, except the innermost two dimensions must be transposed).

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, rtol: float | TArray | None = None) -> TArray: ...


@runtime_checkable
class qr[TArray: Array](Protocol):
    r"""
    Returns the QR decomposition of a full column rank matrix (or a stack of matrices).

    If ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    The **complete QR decomposition** of a matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as

    .. math::
       x = QR

    where :math:`Q \\in\\ \\mathbb{K}^{m \\times m}` is orthogonal when ``x`` is real-valued and unitary when ``x`` is complex-valued and where :math:`R \\in\\ \\mathbb{K}^{m \\times n}` is an upper triangular matrix with real diagonal (even when ``x`` is complex-valued).

    When :math:`m \\gt n` (tall matrix), as :math:`R` is upper triangular, the last :math:`m - n` rows are zero. In this case, the last :math:`m - n` columns of :math:`Q` can be dropped to form the **reduced QR decomposition**.

    .. math::
       x = QR

    where :math:`Q \\in\\ \\mathbb{K}^{m \\times n}` and :math:`R \\in\\ \\mathbb{K}^{n \\times n}`.

    The reduced QR decomposition equals with the complete QR decomposition when :math:`n \\geq m` (wide matrix).

    When ``x`` is a stack of matrices, the function must compute the QR decomposition for each matrix in the stack.

    .. note::
       Whether an array library explicitly checks whether an input array is a full column rank matrix (or a stack of full column rank matrices) is implementation-defined.

    .. warning::
       The elements in the diagonal of :math:`R` are not necessarily positive. Accordingly, the returned QR decomposition is only unique up to the sign of the diagonal of :math:`R`, and different libraries or inputs on different devices may produce different valid decompositions.

    .. warning::
       The QR decomposition is only well-defined if the first ``k = min(m,n)`` columns of every matrix in ``x`` are linearly independent.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices of rank ``N``. Should have a floating-point data type.
    mode: Literal['reduced', 'complete']
        decomposition mode. Should be one of the following modes:

        -   ``'reduced'``: compute only the leading ``K`` columns of ``q``, such that ``q`` and ``r`` have dimensions ``(..., M, K)`` and ``(..., K, N)``, respectively, and where ``K = min(M, N)``.
        -   ``'complete'``: compute ``q`` and ``r`` with dimensions ``(..., M, M)`` and ``(..., M, N)``, respectively.

        Default: ``'reduced'``.

    Returns
    -------
    out: Tuple[array, array]
        a namedtuple ``(Q, R)`` whose

        -   first element must have the field name ``Q`` and must be an array whose shape depends on the value of ``mode`` and contain matrices with orthonormal columns. If ``mode`` is ``'complete'``, the array must have shape ``(..., M, M)``. If ``mode`` is ``'reduced'``, the array must have shape ``(..., M, K)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same size as those of the input array ``x``.
        -   second element must have the field name ``R`` and must be an array whose shape depends on the value of ``mode`` and contain upper-triangular matrices. If ``mode`` is ``'complete'``, the array must have shape ``(..., M, N)``. If ``mode`` is ``'reduced'``, the array must have shape ``(..., K, N)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same size as those of the input ``x``.

        Each returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, mode: Literal["reduced", "complete"] = "reduced") -> tuple[TArray, TArray]: ...


@runtime_checkable
class slogdet[TArray: Array](Protocol):
    r"""
    Returns the sign and the natural logarithm of the absolute value of the determinant of a square matrix (or a stack of square matrices) ``x``.

    .. note::
       The purpose of this function is to calculate the determinant more accurately when the determinant is either very small or very large, as calling ``det`` may overflow or underflow.

    The sign of the determinant is given by

    .. math::
       \\operatorname{sign}(\\det x) = \\begin{cases}
       0 & \\textrm{if } \\det x = 0 \\\\
       \\frac{\\det x}{|\\det x|} & \\textrm{otherwise}
       \\end{cases}

    where :math:`|\\det x|` is the absolute value of the determinant of ``x``.

    When ``x`` is a stack of matrices, the function must compute the sign and natural logarithm of the absolute value of the determinant for each matrix in the stack.

    **Special Cases**

    For real-valued floating-point operands,

    - If the determinant is zero, the ``sign`` should be ``0`` and ``logabsdet`` should be ``-infinity``.

    For complex floating-point operands,

    - If the determinant is ``0 + 0j``, the ``sign`` should be ``0 + 0j`` and ``logabsdet`` should be ``-infinity + 0j``.

    .. note::
       Depending on the underlying algorithm, when the determinant is zero, the returned result may differ from ``-infinity`` (or ``-infinity + 0j``). In all cases, the determinant should be equal to ``sign * exp(logabsdet)`` (although, again, the result may be subject to numerical precision errors).

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.

    Returns
    -------
    out: Tuple[array, array]
        a namedtuple (``sign``, ``logabsdet``) whose

        -   first element must have the field name ``sign`` and must be an array containing a number representing the sign of the determinant for each square matrix. Must have the same data type as ``x``.
        -   second element must have the field name ``logabsdet`` and must be an array containing the natural logarithm of the absolute value of the determinant for each square matrix. If ``x`` is real-valued, the returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`. If ``x`` is complex, the returned array must have a real-valued floating-point data type having the same precision as ``x`` (e.g., if ``x`` is ``complex64``, ``logabsdet`` must have a ``float32`` data type).

        Each returned array must have shape ``shape(x)[:-2]``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> tuple[TArray, TArray]: ...


@runtime_checkable
class solve[TArray: Array](Protocol):
    r"""
    Returns the solution of a square system of linear equations with a unique solution.

    Let ``x1`` equal :math:`A` and ``x2`` equal :math:`B`. If the promoted data type of ``x1`` and ``x2`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if the promoted data type of ``x1`` and ``x2`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    This function computes the solution :math:`X \\in\\ \\mathbb{K}^{m \\times k}` of the **linear system** associated to :math:`A \\in\\ \\mathbb{K}^{m \\times m}` and :math:`B \\in\\ \\mathbb{K}^{m \\times k}` and is defined as

    .. math::
       AX = B

    This system of linear equations has a unique solution if and only if :math:`A` is invertible.

    .. note::
       Whether an array library explicitly checks whether ``x1`` is invertible is implementation-defined.

    When ``x1`` and/or ``x2`` is a stack of matrices, the function must compute a solution for each matrix in the stack.

    Parameters
    ----------
    x1: array
        coefficient array ``A`` having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Must be of full rank (i.e., all rows or, equivalently, columns must be linearly independent). Should have a floating-point data type.
    x2: array
        ordinate (or "dependent variable") array ``B``. If ``x2`` has shape ``(M,)``, ``x2`` is equivalent to an array having shape ``(..., M, 1)``. If ``x2`` has shape ``(..., M, K)``, each column ``k`` defines a set of ordinate values for which to compute a solution, and ``shape(x2)[:-2]`` must be compatible with ``shape(x1)[:-2]`` (see :ref:`broadcasting`). Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the solution to the system ``AX = B`` for each square matrix. If ``x2`` has shape ``(M,)``, the returned array must have shape equal to ``shape(x1)[:-2] + shape(x2)[-1:]``. Otherwise, if ``x2`` has shape ``(..., M, K)```, the returned array must have shape equal to ``(..., M, K)``, where ``...`` refers to the result of broadcasting ``shape(x1)[:-2]`` and ``shape(x2)[:-2]``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class svd[TArray: Array](Protocol):
    r"""
    Returns a singular value decomposition (SVD) of a matrix (or a stack of matrices) ``x``.

    If ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.

    The full **singular value decomposition** of an :math:`m \\times n` matrix :math:`x \\in\\ \\mathbb{K}^{m \\times n}` is a factorization of the form

    .. math::
       x = U \\Sigma V^H

    where :math:`U \\in\\ \\mathbb{K}^{m \\times m}`, :math:`\\Sigma \\in\\ \\mathbb{K}^{m \\times\\ n}`, :math:`\\operatorname{diag}(\\Sigma) \\in\\ \\mathbb{R}^{k}` with :math:`k = \\operatorname{min}(m, n)`, :math:`V^H \\in\\ \\mathbb{K}^{n \\times n}`, and where :math:`V^H` is the conjugate transpose when :math:`V` is complex and the transpose when :math:`V` is real-valued. When ``x`` is real-valued, :math:`U`, :math:`V` (and thus :math:`V^H`) are orthogonal, and, when ``x`` is complex, :math:`U`, :math:`V` (and thus :math:`V^H`) are unitary.

    When :math:`m \\gt n` (tall matrix), we can drop the last :math:`m - n` columns of :math:`U` to form the reduced SVD

    .. math::
       x = U \\Sigma V^H

    where :math:`U \\in\\ \\mathbb{K}^{m \\times k}`, :math:`\\Sigma \\in\\ \\mathbb{K}^{k \\times\\ k}`, :math:`\\operatorname{diag}(\\Sigma) \\in\\ \\mathbb{R}^{k}`, and :math:`V^H \\in\\ \\mathbb{K}^{k \\times n}`. In this case, :math:`U` and :math:`V` have orthonormal columns.

    Similarly, when :math:`n \\gt m` (wide matrix), we can drop the last :math:`n - m` columns of :math:`V` to also form a reduced SVD.

    This function returns the decomposition :math:`U`, :math:`S`, and :math:`V^H`, where :math:`S = \\operatorname{diag}(\\Sigma)`.

    When ``x`` is a stack of matrices, the function must compute the singular value decomposition for each matrix in the stack.

    .. warning::
       The returned arrays :math:`U` and :math:`V` are neither unique nor continuous with respect to ``x``. Because :math:`U` and :math:`V` are not unique, different hardware and software may compute different singular vectors.

       Non-uniqueness stems from the fact that multiplying any pair of singular vectors :math:`u_k`, :math:`v_k` by :math:`-1` when ``x`` is real-valued and by :math:`e^{\\phi j}` (:math:`\\phi \\in \\mathbb{R}`) when ``x`` is complex produces another two valid singular vectors of the matrix.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form matrices on which to perform singular value decomposition. Should have a floating-point data type.
    full_matrices: bool
        If ``True``, compute full-sized ``U`` and ``Vh``, such that ``U`` has shape ``(..., M, M)`` and ``Vh`` has shape ``(..., N, N)``. If ``False``, compute on the leading ``K`` singular vectors, such that ``U`` has shape ``(..., M, K)`` and ``Vh`` has shape ``(..., K, N)`` and where ``K = min(M, N)``. Default: ``True``.

    Returns
    -------
    out: Tuple[array, array, array]
        a namedtuple ``(U, S, Vh)`` whose

        -   first element must have the field name ``U`` and must be an array whose shape depends on the value of ``full_matrices`` and contain matrices with orthonormal columns (i.e., the columns are left singular vectors). If ``full_matrices`` is ``True``, the array must have shape ``(..., M, M)``. If ``full_matrices`` is ``False``, the array must have shape ``(..., M, K)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. Must have the same data type as ``x``.
        -   second element must have the field name ``S`` and must be an array with shape ``(..., K)`` that contains the vector(s) of singular values of length ``K``, where ``K = min(M, N)``. For each vector, the singular values must be sorted in descending order by magnitude, such that ``s[..., 0]`` is the largest value, ``s[..., 1]`` is the second largest value, et cetera. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. Must have a real-valued floating-point data type having the same precision as ``x`` (e.g., if ``x`` is ``complex64``, ``S`` must have a ``float32`` data type).
        -   third element must have the field name ``Vh`` and must be an array whose shape depends on the value of ``full_matrices`` and contain orthonormal rows (i.e., the rows are the right singular vectors and the array is the adjoint). If ``full_matrices`` is ``True``, the array must have shape ``(..., N, N)``. If ``full_matrices`` is ``False``, the array must have shape ``(..., K, N)`` where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. Must have the same data type as ``x``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, full_matrices: bool = True) -> tuple[TArray, TArray, TArray]: ...


@runtime_checkable
class svdvals[TArray: Array](Protocol):
    """
    Returns the singular values of a matrix (or a stack of matrices) ``x``.

    When ``x`` is a stack of matrices, the function must compute the singular values for each matrix in the stack.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form matrices on which to perform singular value decomposition. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array with shape ``(..., K)`` that contains the vector(s) of singular values of length ``K``, where ``K = min(M, N)``. For each vector, the singular values must be sorted in descending order by magnitude, such that ``s[..., 0]`` is the largest value, ``s[..., 1]`` is the second largest value, et cetera. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. The returned array must have a real-valued floating-point data type having the same precision as ``x`` (e.g., if ``x`` is ``complex64``, the returned array must have a ``float32`` data type).

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class trace[TArray: Array, TDtype](Protocol):
    """
    Returns the sum along the specified diagonals of a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a numeric data type.
    offset: int
        offset specifying the off-diagonal relative to the main diagonal.

        -   ``offset = 0``: the main diagonal.
        -   ``offset > 0``: off-diagonal above the main diagonal.
        -   ``offset < 0``: off-diagonal below the main diagonal.

        Default: ``0``.
    dtype: Optional[dtype]
        data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:

        -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.
        -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).

        If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.

    Returns
    -------
    out: array
        an array containing the traces and whose shape is determined by removing the last two dimensions and storing the traces in the last array dimension. For example, if ``x`` has rank ``k`` and shape ``(I, J, K, ..., L, M, N)``, then an output array has rank ``k-2`` and shape ``(I, J, K, ..., L)`` where

        ::

          out[i, j, k, ..., l] = trace(a[i, j, k, ..., l, :, :])

        The returned array must have a data type as described by the ``dtype`` parameter above.

    Notes
    -----
    **Special Cases**

    Let ``N`` equal the number of elements over which to compute the sum.

    -   If ``N`` is ``0``, the sum is ``0`` (i.e., the empty sum).

    For both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.add`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Required the function to return a floating-point array having the same data type as the input array when provided a floating-point array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, offset: int = 0, dtype: TDtype | None = None) -> TArray: ...


@runtime_checkable
class vector_norm[TArray: Array](Protocol):
    r"""
    Computes the vector norm of a vector (or batch of vectors) ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.
    axis: Optional[Union[int, Tuple[int, ...]]]
        If an integer, ``axis`` specifies the axis (dimension) along which to compute vector norms. If an n-tuple, ``axis`` specifies the axes (dimensions) along which to compute batched vector norms. If ``None``, the vector norm must be computed over all array values (i.e., equivalent to computing the vector norm of a flattened array). Negative indices must be supported. Default: ``None``.
    keepdims: bool
        If ``True``, the axes (dimensions) specified by ``axis`` must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the axes (dimensions) specified by ``axis`` must not be included in the result. Default: ``False``.
    ord: Union[int, float, Literal[inf, -inf]]
        order of the norm. The following mathematical norms must be supported:

        +------------------+----------------------------+
        | ord              | description                |
        +==================+============================+
        | 1                | L1-norm (Manhattan)        |
        +------------------+----------------------------+
        | 2                | L2-norm (Euclidean)        |
        +------------------+----------------------------+
        | inf              | infinity norm              |
        +------------------+----------------------------+
        | (int,float >= 1) | p-norm                     |
        +------------------+----------------------------+

        The following non-mathematical "norms" must be supported:

        +------------------+--------------------------------+
        | ord              | description                    |
        +==================+================================+
        | 0                | sum(a != 0)                    |
        +------------------+--------------------------------+
        | -1               | 1./sum(1./abs(a))              |
        +------------------+--------------------------------+
        | -2               | 1./sqrt(sum(1./abs(a)\\*\\*2))   |
        +------------------+--------------------------------+
        | -inf             | min(abs(a))                    |
        +------------------+--------------------------------+
        | (int,float < 1)  | sum(abs(a)\\*\\*ord)\\*\\*(1./ord) |
        +------------------+--------------------------------+

        Default: ``2``.

    Returns
    -------
    out: array
        an array containing the vector norms. If ``axis`` is ``None``, the returned array must be a zero-dimensional array containing a vector norm. If ``axis`` is a scalar value (``int`` or ``float``), the returned array must have a rank which is one less than the rank of ``x``. If ``axis`` is a ``n``-tuple, the returned array must have a rank which is ``n`` less than the rank of ``x``. If ``x`` has a real-valued data type, the returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`. If ``x`` has a complex-valued data type, the returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type).

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False, ord: int | float | Literal[inf, -inf] = 2) -> TArray:  # type: ignore[valid-type]
        ...


@runtime_checkable
class argsort[TArray: Array](Protocol):
    """
    Returns the indices that sort an array ``x`` along a specified axis.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x : array
        input array. Should have a real-valued data type.
    axis: int
        axis along which to sort. If set to ``-1``, the function must sort along the last axis. Default: ``-1``.
    descending: bool
        sort order. If ``True``, the returned indices sort ``x`` in descending order (by value). If ``False``, the returned indices sort ``x`` in ascending order (by value). Default: ``False``.
    stable: bool
        sort stability. If ``True``, the returned indices must maintain the relative order of ``x`` values which compare as equal. If ``False``, the returned indices may or may not maintain the relative order of ``x`` values which compare as equal (i.e., the relative order of ``x`` values which compare as equal is implementation-dependent). Default: ``True``.

    Returns
    -------
    out : array
        an array of indices. The returned array must have the same shape as ``x``. The returned array must have the default array index data type.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int = -1, descending: bool = False, stable: bool = True) -> TArray: ...


@runtime_checkable
class sort[TArray: Array](Protocol):
    """
    Returns a sorted copy of an input array ``x``.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.
    axis: int
        axis along which to sort. If set to ``-1``, the function must sort along the last axis. Default: ``-1``.
    descending: bool
        sort order. If ``True``, the array must be sorted in descending order (by value). If ``False``, the array must be sorted in ascending order (by value). Default: ``False``.
    stable: bool
        sort stability. If ``True``, the returned array must maintain the relative order of ``x`` values which compare as equal. If ``False``, the returned array may or may not maintain the relative order of ``x`` values which compare as equal (i.e., the relative order of ``x`` values which compare as equal is implementation-dependent). Default: ``True``.

    Returns
    -------
    out : array
        a sorted array. The returned array must have the same data type and shape as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int = -1, descending: bool = False, stable: bool = True) -> TArray: ...


@runtime_checkable
class abs[TArray: Array](Protocol):
    r"""
    Calculates the absolute value for each element ``x_i`` of the input array ``x``.

    For real-valued input arrays, the element-wise result has the same magnitude as the respective element in ``x`` but has positive sign.

    .. note::
       For signed integer data types, the absolute value of the minimum representable integer is implementation-dependent.

    .. note::
       For complex floating-point operands, the complex absolute value is known as the norm, modulus, or magnitude and, for a complex number :math:`z = a + bj` is computed as

       .. math::
          \\operatorname{abs}(z) = \\sqrt{a^2 + b^2}

    .. note::
       For complex floating-point operands, conforming implementations should take care to avoid undue overflow or underflow during intermediate stages of computation.

    ..
       TODO: once ``hypot`` is added to the specification, remove the special cases for complex floating-point operands and the note concerning guarding against undue overflow/underflow, and state that special cases must be handled as if implemented as ``hypot(real(x), imag(x))``.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the absolute value of each element in ``x``. If ``x`` has a real-valued data type, the returned array must have the same data type as ``x``. If ``x`` has a complex floating-point data type, the returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type).

    Notes
    -----
    **Special Cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``-0``, the result is ``+0``.
    - If ``x_i`` is ``-infinity``, the result is ``+infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is any value (including ``NaN``), the result is ``+infinity``.
    - If ``a`` is any value (including ``NaN``) and ``b`` is either ``+infinity`` or ``-infinity``, the result is ``+infinity``.
    - If ``a`` is either ``+0`` or ``-0``, the result is equal to ``abs(b)``.
    - If ``b`` is either ``+0`` or ``-0``, the result is equal to ``abs(a)``.
    - If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class acos[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation of the principal value of the inverse cosine for each element ``x_i`` of the input array ``x``.

    Each element-wise result is expressed in radians.

    .. note::
       The principal value of the arc cosine of a complex number :math:`z` is

       .. math::
          \\operatorname{acos}(z) = \\frac{1}{2}\\pi + j\\ \\ln(zj + \\sqrt{1-z^2})

       For any :math:`z`,

       .. math::
          \\operatorname{acos}(z) = \\pi - \\operatorname{acos}(-z)

    .. note::
       For complex floating-point operands, ``acos(conj(x))`` must equal ``conj(acos(x))``.

    .. note::
       The inverse cosine (or arc cosine) is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty, -1)` and :math:`(1, \\infty)` of the real axis.

       Accordingly, for complex arguments, the function returns the inverse cosine in the range of a strip unbounded along the imaginary axis and in the interval :math:`[0, \\pi]` along the real axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is greater than ``1``, the result is ``NaN``.
    - If ``x_i`` is less than ``-1``, the result is ``NaN``.
    - If ``x_i`` is ``1``, the result is ``+0``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``π/2 - 0j``.
    - If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``NaN``, the result is ``π/2 + NaN j``.
    - If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``π/2 - infinity j``.
    - If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``π - infinity j``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+0 - infinity j``.
    - If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``3π/4 - infinity j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``π/4 - infinity j``.
    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``NaN ± infinity j`` (sign of the imaginary component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``NaN - infinity j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class acosh[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the inverse hyperbolic cosine for each element ``x_i`` of the input array ``x``.

    .. note::
       The principal value of the inverse hyperbolic cosine of a complex number :math:`z` is

       .. math::
          \\operatorname{acosh}(z) = \\ln(z + \\sqrt{z+1}\\sqrt{z-1})

       For any :math:`z`,

       .. math::
          \\operatorname{acosh}(z) = \\frac{\\sqrt{z-1}}{\\sqrt{1-z}}\\operatorname{acos}(z)

       or simply

       .. math::
          \\operatorname{acosh}(z) = j\\ \\operatorname{acos}(z)

       in the upper half of the complex plane.

    .. note::
       For complex floating-point operands, ``acosh(conj(x))`` must equal ``conj(acosh(x))``.

    .. note::
       The inverse hyperbolic cosine is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segment :math:`(-\\infty, 1)` of the real axis.

       Accordingly, for complex arguments, the function returns the inverse hyperbolic cosine in the interval :math:`[0, \\infty)` along the real axis and in the interval :math:`[-\\pi j, +\\pi j]` along the imaginary axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array whose elements each represent the area of a hyperbolic sector. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse hyperbolic cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``1``, the result is ``NaN``.
    - If ``x_i`` is ``1``, the result is ``+0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``+0 + πj/2``.
    - If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.
    - If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``NaN ± πj/2`` (sign of imaginary component is unspecified).
    - If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + πj``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.
    - If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + 3πj/4``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.
    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class add[TArray: Array](Protocol):
    """
    Calculates the sum for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. Should have a numeric data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the element-wise sums. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``-infinity``, the result is ``NaN``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``+infinity``, the result is ``NaN``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``-infinity``, the result is ``-infinity``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a finite number, the result is ``+infinity``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a finite number, the result is ``-infinity``.
    - If ``x1_i`` is a finite number and ``x2_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x1_i`` is a finite number and ``x2_i`` is ``-infinity``, the result is ``-infinity``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is ``-0``, the result is ``-0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is ``+0``, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is ``-0``, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is ``+0``, the result is ``+0``.
    - If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is a nonzero finite number, the result is ``x2_i``.
    - If ``x1_i`` is a nonzero finite number and ``x2_i`` is either ``+0`` or ``-0``, the result is ``x1_i``.
    - If ``x1_i`` is a nonzero finite number and ``x2_i`` is ``-x1_i``, the result is ``+0``.
    - In the remaining cases, when neither ``infinity``, ``+0``, ``-0``, nor a ``NaN`` is involved, and the operands have the same mathematical sign or have different magnitudes, the sum must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported round mode. If the magnitude is too large to represent, the operation overflows and the result is an `infinity` of appropriate mathematical sign.

    .. note::
       Floating-point addition is a commutative operation, but not always associative.

    For complex floating-point operands, addition is defined according to the following table. For real components ``a`` and ``c`` and imaginary components ``b`` and ``d``,

    +------------+------------+------------+----------------+
    |            | c          | dj         | c + dj         |
    +============+============+============+================+
    | **a**      | a + c      | a + dj     | (a+c) + dj     |
    +------------+------------+------------+----------------+
    | **bj**     | c + bj     | (b+d)j     | c + (b+d)j     |
    +------------+------------+------------+----------------+
    | **a + bj** | (a+c) + bj | a + (b+d)j | (a+c) + (b+d)j |
    +------------+------------+------------+----------------+

    For complex floating-point operands, real-valued floating-point special cases must independently apply to the real and imaginary component operations involving real numbers as described in the above table. For example, let ``a = real(x1_i)``, ``b = imag(x1_i)``, ``c = real(x2_i)``, ``d = imag(x2_i)``, and

    - If ``a`` is ``-0`` and ``c`` is ``-0``, the real component of the result is ``-0``.
    - Similarly, if ``b`` is ``+0`` and ``d`` is ``-0``, the imaginary component of the result is ``+0``.

    Hence, if ``z1 = a + bj = -0 + 0j`` and ``z2 = c + dj = -0 - 0j``, the result of ``z1 + z2`` is ``-0 + 0j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class asin[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation of the principal value of the inverse sine for each element ``x_i`` of the input array ``x``.

    Each element-wise result is expressed in radians.

    .. note::
       The principal value of the arc sine of a complex number :math:`z` is

       .. math::
          \\operatorname{asin}(z) = -j\\ \\ln(zj + \\sqrt{1-z^2})

       For any :math:`z`,

       .. math::
          \\operatorname{asin}(z) = \\operatorname{acos}(-z) - \\frac{\\pi}{2}

    .. note::
       For complex floating-point operands, ``asin(conj(x))`` must equal ``conj(asin(x))``.

    .. note::
       The inverse sine (or arc sine) is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty, -1)` and :math:`(1, \\infty)` of the real axis.

       Accordingly, for complex arguments, the function returns the inverse sine in the range of a strip unbounded along the imaginary axis and in the interval :math:`[-\\pi/2, +\\pi/2]` along the real axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is greater than ``1``, the result is ``NaN``.
    - If ``x_i`` is less than ``-1``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * asinh(x*1j)``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class asinh[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the inverse hyperbolic sine for each element ``x_i`` in the input array ``x``.

    .. note::
       The principal value of the inverse hyperbolic sine of a complex number :math:`z` is

       .. math::
          \\operatorname{asinh}(z) = \\ln(z + \\sqrt{1+z^2})

       For any :math:`z`,

       .. math::
          \\operatorname{asinh}(z) = \\frac{\\operatorname{asin}(zj)}{j}

    .. note::
       For complex floating-point operands, ``asinh(conj(x))`` must equal ``conj(asinh(x))`` and ``asinh(-z)`` must equal ``-asinh(z)``.

    .. note::
       The inverse hyperbolic sine is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty j, -j)` and :math:`(j, \\infty j)` of the imaginary axis.

       Accordingly, for complex arguments, the function returns the inverse hyperbolic sine in the range of a strip unbounded along the real axis and in the interval :math:`[-\\pi j/2, +\\pi j/2]` along the imaginary axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array whose elements each represent the area of a hyperbolic sector. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse hyperbolic sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.
    - If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.
    - If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.
    - If ``a`` is ``NaN`` and ``b`` is a nonzero finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``±infinity + NaN j`` (sign of the real component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class atan[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation of the principal value of the inverse tangent for each element ``x_i`` of the input array ``x``.

    Each element-wise result is expressed in radians.

    .. note::
       The principal value of the inverse tangent of a complex number :math:`z` is

       .. math::
          \\operatorname{atan}(z) = -\\frac{\\ln(1 - zj) - \\ln(1 + zj)}{2}j

    .. note::
       For complex floating-point operands, ``atan(conj(x))`` must equal ``conj(atan(x))``.

    .. note::
       The inverse tangent (or arc tangent) is a multi-valued function and requires a branch on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty j, -j)` and :math:`(+j, \\infty j)` of the imaginary axis.

       Accordingly, for complex arguments, the function returns the inverse tangent in the range of a strip unbounded along the imaginary axis and in the interval :math:`[-\\pi/2, +\\pi/2]` along the real axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+infinity``, the result is an implementation-dependent approximation to ``+π/2``.
    - If ``x_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``-π/2``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * atanh(x*1j)``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class atan2[TArray: Array](Protocol):
    """
    Calculates an implementation-dependent approximation of the inverse tangent of the quotient ``x1/x2``, having domain ``[-infinity, +infinity] x [-infinity, +infinity]`` (where the ``x`` notation denotes the set of ordered pairs of elements ``(x1_i, x2_i)``) and codomain ``[-π, +π]``, for each pair of elements ``(x1_i, x2_i)`` of the input arrays ``x1`` and ``x2``, respectively. Each element-wise result is expressed in radians.

    The mathematical signs of ``x1_i`` and ``x2_i`` determine the quadrant of each element-wise result. The quadrant (i.e., branch) is chosen such that each element-wise result is the signed angle in radians between the ray ending at the origin and passing through the point ``(1,0)`` and the ray ending at the origin and passing through the point ``(x2_i, x1_i)``.

    .. note::
       Note the role reversal: the "y-coordinate" is the first function parameter; the "x-coordinate" is the second function parameter. The parameter order is intentional and traditional for the two-argument inverse tangent function where the y-coordinate argument is first and the x-coordinate argument is second.

    By IEEE 754 convention, the inverse tangent of the quotient ``x1/x2`` is defined for ``x2_i`` equal to positive or negative zero and for either or both of ``x1_i`` and ``x2_i`` equal to positive or negative ``infinity``.

    Parameters
    ----------
    x1: array
        input array corresponding to the y-coordinates. Should have a real-valued floating-point data type.
    x2: array
        input array corresponding to the x-coordinates. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse tangent of the quotient ``x1/x2``. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is an implementation-dependent approximation to ``+π/2``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``+π/2``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is ``+0``, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``+π``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is an implementation-dependent approximation to ``+π``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``-0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is ``+0``, the result is ``-0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``-π``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is an implementation-dependent approximation to ``-π``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is an implementation-dependent approximation to ``-π/2``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``-π/2``.
    - If ``x1_i`` is greater than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``+infinity``, the result is ``+0``.
    - If ``x1_i`` is greater than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``+π``.
    - If ``x1_i`` is less than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``+infinity``, the result is ``-0``.
    - If ``x1_i`` is less than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``-π``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a finite number, the result is an implementation-dependent approximation to ``+π/2``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a finite number, the result is an implementation-dependent approximation to ``-π/2``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``+infinity``, the result is an implementation-dependent approximation to ``+π/4``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``+3π/4``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``+infinity``, the result is an implementation-dependent approximation to ``-π/4``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``-3π/4``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class atanh[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the inverse hyperbolic tangent for each element ``x_i`` of the input array ``x``.

    .. note::
       The principal value of the inverse hyperbolic tangent of a complex number :math:`z` is

       .. math::
          \\operatorname{atanh}(z) = \\frac{\\ln(1+z)-\\ln(z-1)}{2}

       For any :math:`z`,

       .. math::
          \\operatorname{atanh}(z) = \\frac{\\operatorname{atan}(zj)}{j}

    .. note::
       For complex floating-point operands, ``atanh(conj(x))`` must equal ``conj(atanh(x))`` and ``atanh(-x)`` must equal ``-atanh(x)``.

    .. note::
       The inverse hyperbolic tangent is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty, 1]` and :math:`[1, \\infty)` of the real axis.

       Accordingly, for complex arguments, the function returns the inverse hyperbolic tangent in the range of a half-strip unbounded along the real axis and in the interval :math:`[-\\pi j/2, +\\pi j/2]` along the imaginary axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array whose elements each represent the area of a hyperbolic sector. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the inverse hyperbolic tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``-1``, the result is ``NaN``.
    - If ``x_i`` is greater than ``1``, the result is ``NaN``.
    - If ``x_i`` is ``-1``, the result is ``-infinity``.
    - If ``x_i`` is ``+1``, the result is ``+infinity``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.
    - If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``+0 + NaN j``.
    - If ``a`` is ``1`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.
    - If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``+infinity``, the result is ``+0 + πj/2``.
    - If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+0 + πj/2``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+0 + πj/2``.
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``+0 + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``±0 + πj/2`` (sign of the real component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class bitwise_and[TArray: Array](Protocol):
    """
    Computes the bitwise AND of the underlying binary representation of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. Should have an integer or boolean data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer or boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class bitwise_left_shift[TArray: Array](Protocol):
    """
    Shifts the bits of each element ``x1_i`` of the input array ``x1`` to the left by appending ``x2_i`` (i.e., the respective element in the input array ``x2``) zeros to the right of ``x1_i``.

    Parameters
    ----------
    x1: array
        first input array. Should have an integer data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer data type. Each element must be greater than or equal to ``0``.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class bitwise_invert[TArray: Array](Protocol):
    """
    Inverts (flips) each bit for each element ``x_i`` of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have an integer or boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have the same data type as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class bitwise_or[TArray: Array](Protocol):
    """
    Computes the bitwise OR of the underlying binary representation of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. Should have an integer or boolean data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer or boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class bitwise_right_shift[TArray: Array](Protocol):
    """
    Shifts the bits of each element ``x1_i`` of the input array ``x1`` to the right according to the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       This operation must be an arithmetic shift (i.e., sign-propagating) and thus equivalent to floor division by a power of two.

    Parameters
    ----------
    x1: array
        first input array. Should have an integer data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer data type. Each element must be greater than or equal to ``0``.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class bitwise_xor[TArray: Array](Protocol):
    """
    Computes the bitwise XOR of the underlying binary representation of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. Should have an integer or boolean data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer or boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class ceil[TArray: Array](Protocol):
    """
    Rounds each element ``x_i`` of the input array ``x`` to the smallest (i.e., closest to ``-infinity``) integer-valued number that is not less than ``x_i``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.

    Notes
    -----
    **Special cases**

    - If ``x_i`` is already integer-valued, the result is ``x_i``.

    For floating-point operands,

    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-infinity``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``NaN``, the result is ``NaN``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class clip[TArray: Array](Protocol):
    """
    Clamps each element ``x_i`` of the input array ``x`` to the range ``[min, max]``.

    Parameters
    ----------
    x: array
      input array. Should have a real-valued data type.
    min: Optional[Union[int, float, array]]
      lower-bound of the range to which to clamp. If ``None``, no lower bound must be applied. Must be compatible with ``x`` and ``max`` (see :ref:`broadcasting`). Should have a real-valued data type. Default: ``None``.
    max: Optional[Union[int, float, array]]
      upper-bound of the range to which to clamp. If ``None``, no upper bound must be applied. Must be compatible with ``x`` and ``min`` (see :ref:`broadcasting`). Should have a real-valued data type. Default: ``None``.

    Returns
    -------
    out: array
      an array containing element-wise results. The returned array must have the same data type as ``x``.

    Notes
    -----
    - If both ``min`` and ``max`` are ``None``, the elements of the returned array must equal the respective elements in ``x``.
    - If a broadcasted element in ``min`` is greater than a corresponding broadcasted element in ``max``, behavior is unspecified and thus implementation-dependent.
    - If ``x`` has an integral data type and a broadcasted element in ``min`` or ``max`` is outside the bounds of the data type of ``x``, behavior is unspecified and thus implementation-dependent.
    - If ``x`` and either ``min`` or ``max`` have different data type kinds (e.g., integer versus floating-point), behavior is unspecified and thus implementation-dependent.
    - For scalar ``min`` and/or ``max``, the scalar values should follow type promotion rules for operations involving arrays and scalar operands (see :ref:`type-promotion`).

    **Special cases**

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``min_i`` is ``NaN``, the result is ``NaN``.
    - If ``max_i`` is ``NaN``, the result is ``NaN``.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, min: int | float | TArray | None = None, max: int | float | TArray | None = None) -> TArray: ...


@runtime_checkable
class conj[TArray: Array](Protocol):
    """
    Returns the complex conjugate for each element ``x_i`` of the input array ``x``.

    For complex numbers of the form

    .. math::
       a + bj

    the complex conjugate is defined as

    .. math::
       a - bj

    Hence, the returned complex conjugates must be computed by negating the imaginary component of each element ``x_i``.

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have the same data type as ``x``.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class copysign[TArray: Array](Protocol):
    """
    Composes a floating-point value with the magnitude of ``x1_i`` and the sign of ``x2_i`` for each element of the input array ``x1``.

    Parameters
    ----------
    x1: array
       input array containing magnitudes. Should have a real-valued floating-point data type.
    x2: array
       input array whose sign bits are applied to the magnitudes of ``x1``. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.

    Returns
    -------
    out: array
       an array containing the element-wise results. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands, let ``|x|`` be the absolute value, and if ``x1_i`` is not ``NaN``,

    - If ``x2_i`` is less than ``0``, the result is ``-|x1_i|``.
    - If ``x2_i`` is ``-0``, the result is ``-|x1_i|``.
    - If ``x2_i`` is ``+0``, the result is ``|x1_i|``.
    - If ``x2_i`` is greater than ``0``, the result is ``|x1_i|``.
    - If ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``1``, the result is ``-|x1_i|``.
    - If ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``0``, the result is ``|x1_i|``.

    - If ``x1_i`` is ``NaN`` and ``x2_i`` is less than ``0``, the result is ``NaN`` with a sign bit of ``1``.
    - If ``x1_i`` is ``NaN`` and ``x2_i`` is ``-0``, the result is ``NaN`` with a sign bit of ``1``.
    - If ``x1_i`` is ``NaN`` and ``x2_i`` is ``+0``, the result is ``NaN`` with a sign bit of ``0``.
    - If ``x1_i`` is ``NaN`` and ``x2_i`` is greater than ``0``, the result is ``NaN`` with a sign bit of ``0``.
    - If ``x1_i`` is ``NaN`` and ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``1``, the result is ``NaN`` with a sign bit of ``1``.
    - If ``x1_i`` is ``NaN`` and ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``0``, the result is ``NaN`` with a sign bit of ``0``.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class cos[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the cosine for each element ``x_i`` of the input array ``x``.

    Each element ``x_i`` is assumed to be expressed in radians.

    .. note::
       The cosine is an entire function on the complex plane and has no branch cuts.

    .. note::
       For complex arguments, the mathematical definition of cosine is

       .. math::
          \\begin{align} \\operatorname{cos}(x) &= \\sum_{n=0}^\\infty \\frac{(-1)^n}{(2n)!} x^{2n} \\\\ &= \\frac{e^{jx} + e^{-jx}}{2} \\\\ &= \\operatorname{cosh}(jx) \\end{align}

       where :math:`\\operatorname{cosh}` is the hyperbolic cosine.

    Parameters
    ----------
    x: array
        input array whose elements are each expressed in radians. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``1``.
    - If ``x_i`` is ``-0``, the result is ``1``.
    - If ``x_i`` is ``+infinity``, the result is ``NaN``.
    - If ``x_i`` is ``-infinity``, the result is ``NaN``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented as ``cosh(x*1j)``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class cosh[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the hyperbolic cosine for each element ``x_i`` in the input array ``x``.

    The mathematical definition of the hyperbolic cosine is

    .. math::
       \\operatorname{cosh}(x) = \\frac{e^x + e^{-x}}{2}

    .. note::
       The hyperbolic cosine is an entire function in the complex plane and has no branch cuts. The function is periodic, with period :math:`2\\pi j`, with respect to the imaginary component.

    Parameters
    ----------
    x: array
        input array whose elements each represent a hyperbolic angle. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the hyperbolic cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    .. note::
       For all operands, ``cosh(x)`` must equal ``cosh(-x)``.

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``1``.
    - If ``x_i`` is ``-0``, the result is ``1``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``+infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    .. note::
       For complex floating-point operands, ``cosh(conj(x))`` must equal ``conj(cosh(x))``.

    - If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``1 + 0j``.
    - If ``a`` is ``+0`` and ``b`` is ``+infinity``, the result is ``NaN + 0j`` (sign of the imaginary component is unspecified).
    - If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``NaN + 0j`` (sign of the imaginary component is unspecified).
    - If ``a`` is a nonzero finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.
    - If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.
    - If ``a`` is ``+infinity`` and ``b`` is a nonzero finite number, the result is ``+infinity * cis(b)``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j`` (sign of the real component is unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is either ``+0`` or ``-0``, the result is ``NaN + 0j`` (sign of the imaginary component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is a nonzero finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    where ``cis(v)`` is ``cos(v) + sin(v)*1j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class divide[TArray: Array](Protocol):
    r"""
    Calculates the division of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       If one or both of the input arrays have integer data types, the result is implementation-dependent, as type promotion between data type "kinds" (e.g., integer versus floating-point) is unspecified.

       Specification-compliant libraries may choose to raise an error or return an array containing the element-wise results. If an array is returned, the array must have a real-valued floating-point data type.

    Parameters
    ----------
    x1: array
        dividend input array. Should have a numeric data type.
    x2: array
        divisor input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.
    - If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``-0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``-0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is ``+0``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is ``+infinity``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is ``-infinity``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is ``-infinity``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is ``+infinity``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``-infinity``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``-infinity``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``+infinity``.
    - If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``+0``.
    - If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``-0``.
    - If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``-0``.
    - If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``+0``.
    - If ``x1_i`` and ``x2_i`` have the same mathematical sign and are both nonzero finite numbers, the result has a positive mathematical sign.
    - If ``x1_i`` and ``x2_i`` have different mathematical signs and are both nonzero finite numbers, the result has a negative mathematical sign.
    - In the remaining cases, where neither ``-infinity``, ``+0``, ``-0``, nor ``NaN`` is involved, the quotient must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported rounding mode. If the magnitude is too large to represent, the operation overflows and the result is an ``infinity`` of appropriate mathematical sign. If the magnitude is too small to represent, the operation underflows and the result is a zero of appropriate mathematical sign.

    For complex floating-point operands, division is defined according to the following table. For real components ``a`` and ``c`` and imaginary components ``b`` and ``d``,

    +------------+----------------+-----------------+--------------------------+
    |            | c              | dj              | c + dj                   |
    +============+================+=================+==========================+
    | **a**      | a / c          | -(a/d)j         | special rules            |
    +------------+----------------+-----------------+--------------------------+
    | **bj**     | (b/c)j         | b/d             | special rules            |
    +------------+----------------+-----------------+--------------------------+
    | **a + bj** | (a/c) + (b/c)j | b/d - (a/d)j    | special rules            |
    +------------+----------------+-----------------+--------------------------+

    In general, for complex floating-point operands, real-valued floating-point special cases must independently apply to the real and imaginary component operations involving real numbers as described in the above table.

    When ``a``, ``b``, ``c``, or ``d`` are all finite numbers (i.e., a value other than ``NaN``, ``+infinity``, or ``-infinity``), division of complex floating-point operands should be computed as if calculated according to the textbook formula for complex number division

    .. math::
       \\frac{a + bj}{c + dj} = \\frac{(ac + bd) + (bc - ad)j}{c^2 + d^2}

    When at least one of ``a``, ``b``, ``c``, or ``d`` is ``NaN``, ``+infinity``, or ``-infinity``,

    - If ``a``, ``b``, ``c``, and ``d`` are all ``NaN``, the result is ``NaN + NaN j``.
    - In the remaining cases, the result is implementation dependent.

    .. note::
       For complex floating-point operands, the results of special cases may be implementation dependent depending on how an implementation chooses to model complex numbers and complex infinity (e.g., complex plane versus Riemann sphere). For those implementations following C99 and its one-infinity model, when at least one component is infinite, even if the other component is ``NaN``, the complex value is infinite, and the usual arithmetic rules do not apply to complex-complex division. In the interest of performance, other implementations may want to avoid the complex branching logic necessary to implement the one-infinity model and choose to implement all complex-complex division according to the textbook formula. Accordingly, special case behavior is unlikely to be consistent across implementations.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class equal[TArray: Array](Protocol):
    """
    Computes the truth value of ``x1_i == x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. May have any data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). May have any data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    Notes
    -----
    **Special Cases**

    For real-valued floating-point operands,

    - If ``x1_i`` is ``NaN`` or ``x2_i`` is ``NaN``, the result is ``False``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``+infinity``, the result is ``True``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``-infinity``, the result is ``True``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``True``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``True``.
    - If ``x1_i`` is a finite number, ``x2_i`` is a finite number, and ``x1_i`` equals ``x2_i``, the result is ``True``.
    - In the remaining cases, the result is ``False``.

    For complex floating-point operands, let ``a = real(x1_i)``, ``b = imag(x1_i)``, ``c = real(x2_i)``, ``d = imag(x2_i)``, and

    - If ``a``, ``b``, ``c``, or ``d`` is ``NaN``, the result is ``False``.
    - In the remaining cases, the result is the logical AND of the equality comparison between the real values ``a`` and ``c`` (real components) and between the real values ``b`` and ``d`` (imaginary components), as described above for real-valued floating-point operands (i.e., ``a == c AND b == d``).

    .. note::
       For discussion of complex number equality, see :ref:`complex-numbers`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class exp[TArray: Array](Protocol):
    """
    Calculates an implementation-dependent approximation to the exponential function for each element ``x_i`` of the input array ``x`` (``e`` raised to the power of ``x_i``, where ``e`` is the base of the natural logarithm).

    .. note::
       For complex floating-point operands, ``exp(conj(x))`` must equal ``conj(exp(x))``.

    .. note::
       The exponential function is an entire function in the complex plane and has no branch cuts.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated exponential function result for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``1``.
    - If ``x_i`` is ``-0``, the result is ``1``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``+0``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``1 + 0j``.
    - If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``infinity + 0j``.
    - If ``a`` is ``-infinity`` and ``b`` is a finite number, the result is ``+0 * cis(b)``.
    - If ``a`` is ``+infinity`` and ``b`` is a nonzero finite number, the result is ``+infinity * cis(b)``.
    - If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``0 + 0j`` (signs of real and imaginary components are unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``infinity + NaN j`` (sign of real component is unspecified).
    - If ``a`` is ``-infinity`` and ``b`` is ``NaN``, the result is ``0 + 0j`` (signs of real and imaginary components are unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``infinity + NaN j`` (sign of real component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.
    - If ``a`` is ``NaN`` and ``b`` is not equal to ``0``, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    where ``cis(v)`` is ``cos(v) + sin(v)*1j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class expm1[TArray: Array](Protocol):
    """
    Calculates an implementation-dependent approximation to ``exp(x)-1`` for each element ``x_i`` of the input array ``x``.

    .. note::
       The purpose of this function is to calculate ``exp(x)-1.0`` more accurately when `x` is close to zero. Accordingly, conforming implementations should avoid implementing this function as simply ``exp(x)-1.0``. See FDLIBM, or some other IEEE 754-2019 compliant mathematical library, for a potential reference implementation.

    .. note::
       For complex floating-point operands, ``expm1(conj(x))`` must equal ``conj(expm1(x))``.

    .. note::
       The exponential function is an entire function in the complex plane and has no branch cuts.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-1``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``0 + 0j``.
    - If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.
    - If ``a`` is ``-infinity`` and ``b`` is a finite number, the result is ``+0 * cis(b) - 1.0``.
    - If ``a`` is ``+infinity`` and ``b`` is a nonzero finite number, the result is ``+infinity * cis(b) - 1.0``.
    - If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``-1 + 0j`` (sign of imaginary component is unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``infinity + NaN j`` (sign of real component is unspecified).
    - If ``a`` is ``-infinity`` and ``b`` is ``NaN``, the result is ``-1 + 0j`` (sign of imaginary component is unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``infinity + NaN j`` (sign of real component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.
    - If ``a`` is ``NaN`` and ``b`` is not equal to ``0``, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    where ``cis(v)`` is ``cos(v) + sin(v)*1j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class floor[TArray: Array](Protocol):
    """
    Rounds each element ``x_i`` of the input array ``x`` to the greatest (i.e., closest to ``+infinity``) integer-valued number that is not greater than ``x_i``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.

    Notes
    -----
    **Special cases**

    - If ``x_i`` is already integer-valued, the result is ``x_i``.

    For floating-point operands,

    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-infinity``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``NaN``, the result is ``NaN``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class floor_divide[TArray: Array](Protocol):
    r"""
    Rounds the result of dividing each element ``x1_i`` of the input array ``x1`` by the respective element ``x2_i`` of the input array ``x2`` to the greatest (i.e., closest to `+infinity`) integer-value number that is not greater than the division result.

    .. note::
       For input arrays which promote to an integer data type, the result of division by zero is unspecified and thus implementation-defined.

    Parameters
    ----------
    x1: array
        dividend input array. Should have a real-valued data type.
    x2: array
        divisor input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    .. note::
       Floor division was introduced in Python via `PEP 238 <https://www.python.org/dev/peps/pep-0238/>`_ with the goal to disambiguate "true division" (i.e., computing an approximation to the mathematical operation of division) from "floor division" (i.e., rounding the result of division toward negative infinity). The former was computed when one of the operands was a ``float``, while the latter was computed when both operands were ``int``\\s. Overloading the ``/`` operator to support both behaviors led to subtle numerical bugs when integers are possible, but not expected.

       To resolve this ambiguity, ``/`` was designated for true division, and ``//`` was designated for floor division. Semantically, floor division was `defined <https://www.python.org/dev/peps/pep-0238/#semantics-of-floor-division>`_ as equivalent to ``a // b == floor(a/b)``; however, special floating-point cases were left ill-defined.

       Accordingly, floor division is not implemented consistently across array libraries for some of the special cases documented below. Namely, when one of the operands is ``infinity``, libraries may diverge with some choosing to strictly follow ``floor(a/b)`` and others choosing to pair ``//`` with ``%`` according to the relation ``b = a % b + b * (a // b)``. The special cases leading to divergent behavior are documented below.

       This specification prefers floor division to match ``floor(divide(x1, x2))`` in order to avoid surprising and unexpected results; however, array libraries may choose to more strictly follow Python behavior.

    For floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.
    - If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``-0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``-0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is ``+0``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is ``+infinity``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is ``-infinity``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is ``-infinity``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is ``+infinity``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``-infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``-infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``+infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)
    - If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``+0``.
    - If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``-0``. (**note**: libraries may return ``-1.0`` to match Python behavior.)
    - If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``-0``. (**note**: libraries may return ``-1.0`` to match Python behavior.)
    - If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``+0``.
    - If ``x1_i`` and ``x2_i`` have the same mathematical sign and are both nonzero finite numbers, the result has a positive mathematical sign.
    - If ``x1_i`` and ``x2_i`` have different mathematical signs and are both nonzero finite numbers, the result has a negative mathematical sign.
    - In the remaining cases, where neither ``-infinity``, ``+0``, ``-0``, nor ``NaN`` is involved, the quotient must be computed and rounded to the greatest (i.e., closest to `+infinity`) representable integer-value number that is not greater than the division result. If the magnitude is too large to represent, the operation overflows and the result is an ``infinity`` of appropriate mathematical sign. If the magnitude is too small to represent, the operation underflows and the result is a zero of appropriate mathematical sign.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class greater[TArray: Array](Protocol):
    """
    Computes the truth value of ``x1_i > x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x1: array
        first input array. Should have a real-valued data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class greater_equal[TArray: Array](Protocol):
    """
    Computes the truth value of ``x1_i >= x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x1: array
        first input array. Should have a real-valued data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class hypot[TArray: Array](Protocol):
    """
    Computes the square root of the sum of squares for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       The value computed by this function may be interpreted as the length of the hypotenuse of a right-angled triangle with sides of length ``x1_i`` and ``x2_i``, the distance of a point ``(x1_i, x2_i)`` from the origin ``(0, 0)``, or the magnitude of a complex number ``x1_i + x2_i * 1j``.

    Parameters
    ----------
    x1: array
       first input array. Should have a real-valued floating-point data type.
    x2: array
       second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.

    Returns
    -------
    out: array
       an array containing the element-wise results. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    The purpose of this function is to avoid underflow and overflow during intermediate stages of computation. Accordingly, conforming implementations should not use naive implementations.

    **Special Cases**

    For real-valued floating-point operands,

    - If ``x1_i`` is ``+infinity`` or ``-infinity`` and ``x2_i`` is any value, including ``NaN``, the result is ``+infinity``.
    - If ``x2_i`` is ``+infinity`` or ``-infinity`` and ``x1_i`` is any value, including ``NaN``, the result is ``+infinity``.
    - If ``x1_i`` is either ``+0`` or ``-0``, the result is equivalent to ``abs(x2_i)``.
    - If ``x2_i`` is either ``+0`` or ``-0``, the result is equivalent to ``abs(x1_i)``.
    - If ``x1_i`` is a finite number or ``NaN`` and ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x2_i`` is a finite number or ``NaN`` and ``x1_i`` is ``NaN``, the result is ``NaN``.
    - Underflow may only occur when both arguments are subnormal and the correct result is also subnormal.

    For real-valued floating-point operands, ``hypot(x1, x2)`` must equal ``hypot(x2, x1)``, ``hypot(x1, -x2)``, ``hypot(-x1, x2)``, and ``hypot(-x1, -x2)``.

    .. note::
       IEEE 754-2019 requires support for subnormal (a.k.a., denormal) numbers, which are useful for supporting gradual underflow. However, hardware support for subnormal numbers is not universal, and many platforms (e.g., accelerators) and compilers support toggling denormals-are-zero (DAZ) and/or flush-to-zero (FTZ) behavior to increase performance and to guard against timing attacks.

       Accordingly, conforming implementations may vary in their support for subnormal numbers.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class imag[TArray: Array](Protocol):
    """
    Returns the imaginary component of a complex number for each element ``x_i`` of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a floating-point data type with the same floating-point precision as ``x`` (e.g., if ``x`` is ``complex64``, the returned array must have the floating-point data type ``float32``).

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class isfinite[TArray: Array](Protocol):
    """
    Tests each element ``x_i`` of the input array ``x`` to determine if finite.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing test results. The returned array must have a data type of ``bool``.

    Notes
    -----
    **Special Cases**

    For real-valued floating-point operands,

    - If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``False``.
    - If ``x_i`` is ``NaN``, the result is ``False``.
    - If ``x_i`` is a finite number, the result is ``True``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is ``NaN`` or ``b`` is ``NaN``, the result is ``False``.
    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is any value, the result is ``False``.
    - If ``a`` is any value and ``b`` is either ``+infinity`` or ``-infinity``, the result is ``False``.
    - If ``a`` is a finite number and ``b`` is a finite number, the result is ``True``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class isinf[TArray: Array](Protocol):
    """
    Tests each element ``x_i`` of the input array ``x`` to determine if equal to positive or negative infinity.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing test results. The returned array must have a data type of ``bool``.

    Notes
    -----
    **Special Cases**

    For real-valued floating-point operands,

    - If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``True``.
    - In the remaining cases, the result is ``False``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is any value (including ``NaN``), the result is ``True``.
    - If ``a`` is either a finite number or ``NaN`` and ``b`` is either ``+infinity`` or ``-infinity``, the result is ``True``.
    - In the remaining cases, the result is ``False``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class isnan[TArray: Array](Protocol):
    """
    Tests each element ``x_i`` of the input array ``x`` to determine whether the element is ``NaN``.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing test results. The returned array should have a data type of ``bool``.

    Notes
    -----
    **Special Cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``True``.
    - In the remaining cases, the result is ``False``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` or ``b`` is ``NaN``, the result is ``True``.
    - In the remaining cases, the result is ``False``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class less[TArray: Array](Protocol):
    """
    Computes the truth value of ``x1_i < x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x1: array
        first input array. Should have a real-valued data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class less_equal[TArray: Array](Protocol):
    """
    Computes the truth value of ``x1_i <= x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x1: array
        first input array. Should have a real-valued data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class log[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the natural (base ``e``) logarithm for each element ``x_i`` of the input array ``x``.

    .. note::
       The natural logarithm of a complex number :math:`z` with polar coordinates :math:`(r,\\theta)` equals :math:`\\ln r + (\\theta + 2n\\pi)j` with principal value :math:`\\ln r + \\theta j`.

    .. note::
       For complex floating-point operands, ``log(conj(x))`` must equal ``conj(log(x))``.

    .. note::
       By convention, the branch cut of the natural logarithm is the negative real axis :math:`(-\\infty, 0)`.

       The natural logarithm is a continuous function from above the branch cut, taking into account the sign of the imaginary component.

       Accordingly, for complex arguments, the function returns the natural logarithm in the range of a strip in the interval :math:`[-\\pi j, +\\pi j]` along the imaginary axis and mathematically unbounded along the real axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated natural logarithm for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``0``, the result is ``NaN``.
    - If ``x_i`` is either ``+0`` or ``-0``, the result is ``-infinity``.
    - If ``x_i`` is ``1``, the result is ``+0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is ``-0`` and ``b`` is ``+0``, the result is ``-infinity + πj``.
    - If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``-infinity + 0j``.
    - If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + πj``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.
    - If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + 3πj/4``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.
    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class log1p[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to ``log(1+x)``, where ``log`` refers to the natural (base ``e``) logarithm, for each element ``x_i`` of the input array ``x``.

    .. note::
       The purpose of this function is to calculate ``log(1+x)`` more accurately when `x` is close to zero. Accordingly, conforming implementations should avoid implementing this function as simply ``log(1+x)``. See FDLIBM, or some other IEEE 754-2019 compliant mathematical library, for a potential reference implementation.

    .. note::
       For complex floating-point operands, ``log1p(conj(x))`` must equal ``conj(log1p(x))``.

    .. note::
       By convention, the branch cut of the natural logarithm is the negative real axis :math:`(-\\infty, 0)`.

       The natural logarithm is a continuous function from above the branch cut, taking into account the sign of the imaginary component.

       Accordingly, for complex arguments, the function returns the natural logarithm in the range of a strip in the interval :math:`[-\\pi j, +\\pi j]` along the imaginary axis and mathematically unbounded along the real axis.

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``-1``, the result is ``NaN``.
    - If ``x_i`` is ``-1``, the result is ``-infinity``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is ``-1`` and ``b`` is ``+0``, the result is ``-infinity + 0j``.
    - If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + πj``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.
    - If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + 3πj/4``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.
    - If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class log2[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the base ``2`` logarithm for each element ``x_i`` of the input array ``x``.

    .. note::
       For complex floating-point operands, ``log2(conj(x))`` must equal ``conj(log2(x))``.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated base ``2`` logarithm for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``0``, the result is ``NaN``.
    - If ``x_i`` is either ``+0`` or ``-0``, the result is ``-infinity``.
    - If ``x_i`` is ``1``, the result is ``+0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented using the standard change of base formula

    .. math::
       \\log_{2} x = \\frac{\\log_{e} x}{\\log_{e} 2}

    where :math:`\\log_{e}` is the natural logarithm, as implemented by :func:`~array_api.log`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class log10[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the base ``10`` logarithm for each element ``x_i`` of the input array ``x``.

    .. note::
       For complex floating-point operands, ``log10(conj(x))`` must equal ``conj(log10(x))``.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated base ``10`` logarithm for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``0``, the result is ``NaN``.
    - If ``x_i`` is either ``+0`` or ``-0``, the result is ``-infinity``.
    - If ``x_i`` is ``1``, the result is ``+0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented using the standard change of base formula

    .. math::
       \\log_{10} x = \\frac{\\log_{e} x}{\\log_{e} 10}

    where :math:`\\log_{e}` is the natural logarithm, as implemented by :func:`~array_api.log`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class logaddexp[TArray: Array](Protocol):
    """
    Calculates the logarithm of the sum of exponentiations ``log(exp(x1) + exp(x2))`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. Should have a real-valued floating-point data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is not ``NaN``, the result is ``+infinity``.
    - If ``x1_i`` is not ``NaN`` and ``x2_i`` is ``+infinity``, the result is ``+infinity``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class logical_and[TArray: Array](Protocol):
    """
    Computes the logical AND for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.

    Parameters
    ----------
    x1: array
        first input array. Should have a boolean data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of `bool`.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class logical_not[TArray: Array](Protocol):
    """
    Computes the logical NOT for each element ``x_i`` of the input array ``x``.

    .. note::
       While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.

    Parameters
    ----------
    x: array
        input array. Should have a boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class logical_or[TArray: Array](Protocol):
    """
    Computes the logical OR for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.

    Parameters
    ----------
    x1: array
        first input array. Should have a boolean data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class logical_xor[TArray: Array](Protocol):
    """
    Computes the logical XOR for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.

    Parameters
    ----------
    x1: array
        first input array. Should have a boolean data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a boolean data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class maximum[TArray: Array](Protocol):
    """
    Computes the maximum value for each element ``x1_i`` of the input array ``x1`` relative to the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
       first input array. Should have a real-valued data type.
    x2: array
       second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
       an array containing the element-wise maximum values. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    The order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a maximum value, specification-compliant libraries may choose to return either value.

    For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).

    **Special Cases**

    For floating-point operands,

    -   If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class minimum[TArray: Array](Protocol):
    """
    Computes the minimum value for each element ``x1_i`` of the input array ``x1`` relative to the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
       first input array. Should have a real-valued data type.
    x2: array
       second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
       an array containing the element-wise minimum values. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    The order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a minimum value, specification-compliant libraries may choose to return either value.

    For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).

    **Special Cases**

    For floating-point operands,

    -   If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class multiply[TArray: Array](Protocol):
    r"""
    Calculates the product for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       Floating-point multiplication is not always associative due to finite precision.

    Parameters
    ----------
    x1: array
        first input array. Should have a numeric data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the element-wise products. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.
    - If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.
    - If ``x1_i`` and ``x2_i`` have the same mathematical sign, the result has a positive mathematical sign, unless the result is ``NaN``. If the result is ``NaN``, the "sign" of ``NaN`` is implementation-defined.
    - If ``x1_i`` and ``x2_i`` have different mathematical signs, the result has a negative mathematical sign, unless the result is ``NaN``. If the result is ``NaN``, the "sign" of ``NaN`` is implementation-defined.
    - If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is a signed infinity with the mathematical sign determined by the rule already stated above.
    - If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is a nonzero finite number, the result is a signed infinity with the mathematical sign determined by the rule already stated above.
    - If ``x1_i`` is a nonzero finite number and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is a signed infinity with the mathematical sign determined by the rule already stated above.
    - In the remaining cases, where neither ``infinity`` nor ``NaN`` is involved, the product must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported rounding mode. If the magnitude is too large to represent, the result is an `infinity` of appropriate mathematical sign. If the magnitude is too small to represent, the result is a zero of appropriate mathematical sign.

    For complex floating-point operands, multiplication is defined according to the following table. For real components ``a`` and ``c`` and imaginary components ``b`` and ``d``,

    +------------+----------------+-----------------+--------------------------+
    |            | c              | dj              | c + dj                   |
    +============+================+=================+==========================+
    | **a**      | a * c          | (a*d)j          | (a*c) + (a*d)j           |
    +------------+----------------+-----------------+--------------------------+
    | **bj**     | (b*c)j         | -(b*d)          | -(b*d) + (b*c)j          |
    +------------+----------------+-----------------+--------------------------+
    | **a + bj** | (a*c) + (b*c)j | -(b*d) + (a*d)j | special rules            |
    +------------+----------------+-----------------+--------------------------+

    In general, for complex floating-point operands, real-valued floating-point special cases must independently apply to the real and imaginary component operations involving real numbers as described in the above table.

    When ``a``, ``b``, ``c``, or ``d`` are all finite numbers (i.e., a value other than ``NaN``, ``+infinity``, or ``-infinity``), multiplication of complex floating-point operands should be computed as if calculated according to the textbook formula for complex number multiplication

    .. math::
       (a + bj) \\cdot (c + dj) = (ac - bd) + (bc + ad)j

    When at least one of ``a``, ``b``, ``c``, or ``d`` is ``NaN``, ``+infinity``, or ``-infinity``,

    - If ``a``, ``b``, ``c``, and ``d`` are all ``NaN``, the result is ``NaN + NaN j``.
    - In the remaining cases, the result is implementation dependent.

    .. note::
       For complex floating-point operands, the results of special cases may be implementation dependent depending on how an implementation chooses to model complex numbers and complex infinity (e.g., complex plane versus Riemann sphere). For those implementations following C99 and its one-infinity model, when at least one component is infinite, even if the other component is ``NaN``, the complex value is infinite, and the usual arithmetic rules do not apply to complex-complex multiplication. In the interest of performance, other implementations may want to avoid the complex branching logic necessary to implement the one-infinity model and choose to implement all complex-complex multiplication according to the textbook formula. Accordingly, special case behavior is unlikely to be consistent across implementations.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class negative[TArray: Array](Protocol):
    """
    Computes the numerical negative of each element ``x_i`` (i.e., ``y_i = -x_i``) of the input array ``x``.

    .. note::
       For signed integer data types, the numerical negative of the minimum representable integer is implementation-dependent.

    .. note::
       If ``x`` has a complex floating-point data type, both the real and imaginary components for each ``x_i`` must be negated (a result which follows from the rules of complex number multiplication).

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class not_equal[TArray: Array](Protocol):
    """
    Computes the truth value of ``x1_i != x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. May have any data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`).

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type of ``bool``.

    Notes
    -----
    **Special Cases**

    For real-valued floating-point operands,

    - If ``x1_i`` is ``NaN`` or ``x2_i`` is ``NaN``, the result is ``True``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``-infinity``, the result is ``True``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``+infinity``, the result is ``True``.
    - If ``x1_i`` is a finite number, ``x2_i`` is a finite number, and ``x1_i`` does not equal ``x2_i``, the result is ``True``.
    - In the remaining cases, the result is ``False``.

    For complex floating-point operands, let ``a = real(x1_i)``, ``b = imag(x1_i)``, ``c = real(x2_i)``, ``d = imag(x2_i)``, and

    - If ``a``, ``b``, ``c``, or ``d`` is ``NaN``, the result is ``True``.
    - In the remaining cases, the result is the logical OR of the equality comparison between the real values ``a`` and ``c`` (real components) and between the real values ``b`` and ``d`` (imaginary components), as described above for real-valued floating-point operands (i.e., ``a != c OR b != d``).

    .. note::
       For discussion of complex number equality, see :ref:`complex-numbers`.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class positive[TArray: Array](Protocol):
    """
    Computes the numerical positive of each element ``x_i`` (i.e., ``y_i = +x_i``) of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have the same data type as ``x``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class pow[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation of exponentiation by raising each element ``x1_i`` (the base) of the input array ``x1`` to the power of ``x2_i`` (the exponent), where ``x2_i`` is the corresponding element of the input array ``x2``.

    .. note::
       If both ``x1`` and ``x2`` have integer data types, the result of ``pow`` when ``x2_i`` is negative (i.e., less than zero) is unspecified and thus implementation-dependent.

       If ``x1`` has an integer data type and ``x2`` has a floating-point data type, behavior is implementation-dependent (type promotion between data type "kinds" (integer versus floating-point) is unspecified).

    .. note::
       By convention, the branch cut of the natural logarithm is the negative real axis :math:`(-\\infty, 0)`.

       The natural logarithm is a continuous function from above the branch cut, taking into account the sign of the imaginary component. As special cases involving complex floating-point operands should be handled according to ``exp(x2*log(x1))``, exponentiation has the same branch cut for ``x1`` as the natural logarithm (see :func:`~array_api.log`).

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x1: array
        first input array whose elements correspond to the exponentiation base. Should have a numeric data type.
    x2: array
        second input array whose elements correspond to the exponentiation exponent. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x1_i`` is not equal to ``1`` and ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x2_i`` is ``+0``, the result is ``1``, even if ``x1_i`` is ``NaN``.
    - If ``x2_i`` is ``-0``, the result is ``1``, even if ``x1_i`` is ``NaN``.
    - If ``x1_i`` is ``NaN`` and ``x2_i`` is not equal to ``0``, the result is ``NaN``.
    - If ``abs(x1_i)`` is greater than ``1`` and ``x2_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``abs(x1_i)`` is greater than ``1`` and ``x2_i`` is ``-infinity``, the result is ``+0``.
    - If ``abs(x1_i)`` is ``1`` and ``x2_i`` is ``+infinity``, the result is ``1``.
    - If ``abs(x1_i)`` is ``1`` and ``x2_i`` is ``-infinity``, the result is ``1``.
    - If ``x1_i`` is ``1`` and ``x2_i`` is not ``NaN``, the result is ``1``.
    - If ``abs(x1_i)`` is less than ``1`` and ``x2_i`` is ``+infinity``, the result is ``+0``.
    - If ``abs(x1_i)`` is less than ``1`` and ``x2_i`` is ``-infinity``, the result is ``+infinity``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is greater than ``0``, the result is ``+infinity``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is less than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``-infinity``, ``x2_i`` is greater than ``0``, and ``x2_i`` is an odd integer value, the result is ``-infinity``.
    - If ``x1_i`` is ``-infinity``, ``x2_i`` is greater than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+infinity``.
    - If ``x1_i`` is ``-infinity``, ``x2_i`` is less than ``0``, and ``x2_i`` is an odd integer value, the result is ``-0``.
    - If ``x1_i`` is ``-infinity``, ``x2_i`` is less than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``+infinity``.
    - If ``x1_i`` is ``-0``, ``x2_i`` is greater than ``0``, and ``x2_i`` is an odd integer value, the result is ``-0``.
    - If ``x1_i`` is ``-0``, ``x2_i`` is greater than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+0``.
    - If ``x1_i`` is ``-0``, ``x2_i`` is less than ``0``, and ``x2_i`` is an odd integer value, the result is ``-infinity``.
    - If ``x1_i`` is ``-0``, ``x2_i`` is less than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+infinity``.
    - If ``x1_i`` is less than ``0``, ``x1_i`` is a finite number, ``x2_i`` is a finite number, and ``x2_i`` is not an integer value, the result is ``NaN``.

    For complex floating-point operands, special cases should be handled as if the operation is implemented as ``exp(x2*log(x1))``.

    .. note::
       Conforming implementations are allowed to treat special cases involving complex floating-point operands more carefully than as described in this specification.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class real[TArray: Array](Protocol):
    """
    Returns the real component of a complex number for each element ``x_i`` of the input array ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must have a floating-point data type with the same floating-point precision as ``x`` (e.g., if ``x`` is ``complex64``, the returned array must have the floating-point data type ``float32``).

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class remainder[TArray: Array](Protocol):
    """
    Returns the remainder of division for each element ``x1_i`` of the input array ``x1`` and the respective element ``x2_i`` of the input array ``x2``.

    .. note::
       This function is equivalent to the Python modulus operator ``x1_i % x2_i``.

    .. note::
       For input arrays which promote to an integer data type, the result of division by zero is unspecified and thus implementation-defined.

    Parameters
    ----------
    x1: array
        dividend input array. Should have a real-valued data type.
    x2: array
        divisor input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. Each element-wise result must have the same sign as the respective element ``x2_i``. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    .. note::
       In general, similar to Python's ``%`` operator, this function is **not** recommended for floating-point operands as semantics do not follow IEEE 754. That this function is specified to accept floating-point operands is primarily for reasons of backward compatibility.

    For floating-point operands,

    - If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.
    - If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.
    - If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.
    - If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``-0``.
    - If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is ``-0``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is ``NaN``.
    - If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is ``NaN``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is ``NaN``.
    - If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is ``NaN``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``NaN``.
    - If ``x1_i`` is ``+infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``NaN``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``NaN``.
    - If ``x1_i`` is ``-infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``NaN``.
    - If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``x1_i``. (**note**: this result matches Python behavior.)
    - If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``x2_i``. (**note**: this result matches Python behavior.)
    - If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``x2_i``. (**note**: this results matches Python behavior.)
    - If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``x1_i``. (**note**: this result matches Python behavior.)
    - In the remaining cases, the result must match that of the Python ``%`` operator.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class round[TArray: Array](Protocol):
    """
    Rounds each element ``x_i`` of the input array ``x`` to the nearest integer-valued number.

    .. note::
       For complex floating-point operands, real and imaginary components must be independently rounded to the nearest integer-valued number.

       Rounded real and imaginary components must be equal to their equivalent rounded real-valued floating-point counterparts (i.e., for complex-valued ``x``, ``real(round(x))`` must equal ``round(real(x)))`` and ``imag(round(x))`` must equal ``round(imag(x))``).

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.

    Notes
    -----
    **Special cases**

    .. note::
       For complex floating-point operands, the following special cases apply to real and imaginary components independently (e.g., if ``real(x_i)`` is ``NaN``, the rounded real component is ``NaN``).

    - If ``x_i`` is already integer-valued, the result is ``x_i``.

    For floating-point operands,

    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-infinity``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If two integers are equally close to ``x_i``, the result is the even integer closest to ``x_i``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class sign[TArray: Array](Protocol):
    r"""
    Returns an indication of the sign of a number for each element ``x_i`` of the input array ``x``.

    The sign function (also known as the **signum function**) of a number :math:`x_i` is defined as

    .. math::
       \\operatorname{sign}(x_i) = \\begin{cases}
       0 & \\textrm{if } x_i = 0 \\\\
       \\frac{x_i}{|x_i|} & \\textrm{otherwise}
       \\end{cases}

    where :math:`|x_i|` is the absolute value of :math:`x_i`.

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have the same data type as ``x``.

    Notes
    -----
    **Special cases**

    For real-valued operands,

    - If ``x_i`` is less than ``0``, the result is ``-1``.
    - If ``x_i`` is either ``-0`` or ``+0``, the result is ``0``.
    - If ``x_i`` is greater than ``0``, the result is ``+1``.
    - If ``x_i`` is ``NaN``, the result is ``NaN``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``-0`` or ``+0`` and ``b`` is either ``-0`` or ``+0``, the result is ``0 + 0j``.
    - If ``a`` is ``NaN`` or ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - In the remaining cases, special cases must be handled according to the rules of complex number division (see :func:`~array_api.divide`).

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class signbit[TArray: Array](Protocol):
    """
    Determines whether the sign bit is set for each element ``x_i`` of the input array ``x``.

    The sign bit of a real-valued floating-point number ``x_i`` is set whenever ``x_i`` is either ``-0``, less than zero, or a signed ``NaN`` (i.e., a ``NaN`` value whose sign bit is ``1``).

    Parameters
    ----------
    x: array
        input array. Should have a real-valued floating-point data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have a data type of ``bool``.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``+0``, the result is ``False``.
    - If ``x_i`` is ``-0``, the result is ``True``.
    - If ``x_i`` is ``+infinity``, the result is ``False``.
    - If ``x_i`` is ``-infinity``, the result is ``True``.
    - If ``x_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``False``.
    - If ``x_i`` is a negative (i.e., less than ``0``) finite number, the result is ``True``.
    - If ``x_i`` is ``NaN`` and the sign bit of ``x_i`` is ``0``, the result is ``False``.
    - If ``x_i`` is ``NaN`` and the sign bit of ``x_i`` is ``1``, the result is ``True``.

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class sin[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the sine for each element ``x_i`` of the input array ``x``.

    Each element ``x_i`` is assumed to be expressed in radians.

    .. note::
       The sine is an entire function on the complex plane and has no branch cuts.

    .. note::
       For complex arguments, the mathematical definition of sine is

       .. math::
          \\begin{align} \\operatorname{sin}(x) &= \\frac{e^{jx} - e^{-jx}}{2j} \\\\ &= \\frac{\\operatorname{sinh}(jx)}{j} \\\\ &= \\frac{\\operatorname{sinh}(jx)}{j} \\cdot \\frac{j}{j} \\\\ &= -j \\cdot \\operatorname{sinh}(jx) \\end{align}

       where :math:`\\operatorname{sinh}` is the hyperbolic sine.

    Parameters
    ----------
    x: array
        input array whose elements are each expressed in radians. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * sinh(x*1j)``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class sinh[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the hyperbolic sine for each element ``x_i`` of the input array ``x``.

    The mathematical definition of the hyperbolic sine is

    .. math::
       \\operatorname{sinh}(x) = \\frac{e^x - e^{-x}}{2}

    .. note::
       The hyperbolic sine is an entire function in the complex plane and has no branch cuts. The function is periodic, with period :math:`2\\pi j`, with respect to the imaginary component.

    Parameters
    ----------
    x: array
        input array whose elements each represent a hyperbolic angle. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the hyperbolic sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    .. note::
       For all operands, ``sinh(x)`` must equal ``-sinh(-x)``.

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    .. note::
       For complex floating-point operands, ``sinh(conj(x))`` must equal ``conj(sinh(x))``.

    - If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.
    - If ``a`` is ``+0`` and ``b`` is ``+infinity``, the result is ``0 + NaN j`` (sign of the real component is unspecified).
    - If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``0 + NaN j`` (sign of the real component is unspecified).
    - If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.
    - If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive finite number, the result is ``+infinity * cis(b)``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``infinity + NaN j`` (sign of the real component is unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``infinity + NaN j`` (sign of the real component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.
    - If ``a`` is ``NaN`` and ``b`` is a nonzero finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    where ``cis(v)`` is ``cos(v) + sin(v)*1j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class square[TArray: Array](Protocol):
    r"""
    Squares each element ``x_i`` of the input array ``x``.

    The square of a number ``x_i`` is defined as

    .. math::
       x_i^2 = x_i \\cdot x_i

    Parameters
    ----------
    x: array
        input array. Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the evaluated result for each element in ``x``. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For floating-point operands, special cases must be handled as if the operation is implemented as ``x * x`` (see :func:`~array_api.multiply`).

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class sqrt[TArray: Array](Protocol):
    r"""
    Calculates the principal square root for each element ``x_i`` of the input array ``x``.

    .. note::
       After rounding, each result must be indistinguishable from the infinitely precise result (as required by IEEE 754).

    .. note::
       For complex floating-point operands, ``sqrt(conj(x))`` must equal ``conj(sqrt(x))``.

    .. note::
       By convention, the branch cut of the square root is the negative real axis :math:`(-\\infty, 0)`.

       The square root is a continuous function from above the branch cut, taking into account the sign of the imaginary component.

       Accordingly, for complex arguments, the function returns the square root in the range of the right half-plane, including the imaginary axis (i.e., the plane defined by :math:`[0, +\\infty)` along the real axis and :math:`(-\\infty, +\\infty)` along the imaginary axis).

       *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the square root of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is less than ``0``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    - If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.
    - If ``a`` is any value (including ``NaN``) and ``b`` is ``+infinity``, the result is ``+infinity + infinity j``.
    - If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``NaN + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+0 + infinity j``.
    - If ``a`` is ``-infinity`` and ``b`` is ``NaN``, the result is ``NaN + infinity j`` (sign of the imaginary component is unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is any value, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class subtract[TArray: Array](Protocol):
    """
    Calculates the difference for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.

    The result of ``x1_i - x2_i`` must be the same as ``x1_i + (-x2_i)`` and must be governed by the same floating-point rules as addition (see :meth:`add`).

    Parameters
    ----------
    x1: array
        first input array. Should have a numeric data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.

    Returns
    -------
    out: array
        an array containing the element-wise differences. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class tan[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the tangent for each element ``x_i`` of the input array ``x``.

    Each element ``x_i`` is assumed to be expressed in radians.

    .. note::
       Tangent is an analytical function on the complex plane and has no branch cuts. The function is periodic, with period :math:`\\pi j`, with respect to the real component and has first order poles along the real line at coordinates :math:`(\\pi (\\frac{1}{2} + n), 0)`. However, IEEE 754 binary floating-point representation cannot represent the value :math:`\\pi / 2` exactly, and, thus, no argument value is possible for which a pole error occurs.

    .. note::
       For complex arguments, the mathematical definition of tangent is

       .. math::
          \\begin{align} \\operatorname{tan}(x) &= \\frac{j(e^{-jx} - e^{jx})}{e^{-jx} + e^{jx}} \\\\ &= (-1) \\frac{j(e^{jx} - e^{-jx})}{e^{jx} + e^{-jx}} \\\\ &= -j \\cdot \\operatorname{tanh}(jx) \\end{align}

       where :math:`\\operatorname{tanh}` is the hyperbolic tangent.

    Parameters
    ----------
    x: array
        input array whose elements are expressed in radians. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.

    For complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * tanh(x*1j)``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class tanh[TArray: Array](Protocol):
    r"""
    Calculates an implementation-dependent approximation to the hyperbolic tangent for each element ``x_i`` of the input array ``x``.

    The mathematical definition of the hyperbolic tangent is

    .. math::
       \\begin{align} \\operatorname{tanh}(x) &= \\frac{\\operatorname{sinh}(x)}{\\operatorname{cosh}(x)} \\\\ &= \\frac{e^x - e^{-x}}{e^x + e^{-x}} \\end{align}

    where :math:`\\operatorname{sinh}(x)` is the hyperbolic sine and :math:`\\operatorname{cosh}(x)` is the hyperbolic cosine.

    .. note::
       The hyperbolic tangent is an analytical function on the complex plane and has no branch cuts. The function is periodic, with period :math:`\\pi j`, with respect to the imaginary component and has first order poles along the imaginary line at coordinates :math:`(0, \\pi (\\frac{1}{2} + n))`. However, IEEE 754 binary floating-point representation cannot represent :math:`\\pi / 2` exactly, and, thus, no argument value is possible such that a pole error occurs.

    Parameters
    ----------
    x: array
        input array whose elements each represent a hyperbolic angle. Should have a floating-point data type.

    Returns
    -------
    out: array
        an array containing the hyperbolic tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Special cases**

    .. note::
       For all operands, ``tanh(-x)`` must equal ``-tanh(x)``.

    For real-valued floating-point operands,

    - If ``x_i`` is ``NaN``, the result is ``NaN``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``+infinity``, the result is ``+1``.
    - If ``x_i`` is ``-infinity``, the result is ``-1``.

    For complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and

    .. note::
       For complex floating-point operands, ``tanh(conj(x))`` must equal ``conj(tanh(x))``.

    - If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.
    - If ``a`` is a nonzero finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+0`` and ``b`` is ``+infinity``, the result is ``+0 + NaN j``.
    - If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.
    - If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``+0 + NaN j``.
    - If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``1 + 0j``.
    - If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``1 + 0j`` (sign of the imaginary component is unspecified).
    - If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``1 + 0j`` (sign of the imaginary component is unspecified).
    - If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.
    - If ``a`` is ``NaN`` and ``b`` is a nonzero number, the result is ``NaN + NaN j``.
    - If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.

    .. warning::
       For historical reasons stemming from the C standard, array libraries may not return the expected result when ``a`` is ``+0`` and ``b`` is either ``+infinity`` or ``NaN``. The result should be ``+0 + NaN j`` in both cases; however, for libraries compiled against older C versions, the result may be ``NaN + NaN j``.

       Array libraries are not required to patch these older C versions, and, thus, users are advised that results may vary across array library implementations for these special cases.

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class trunc[TArray: Array](Protocol):
    """
    Rounds each element ``x_i`` of the input array ``x`` to the nearest integer-valued number that is closer to zero than ``x_i``.

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.

    Returns
    -------
    out: array
        an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.

    Notes
    -----
    **Special cases**

    - If ``x_i`` is already integer-valued, the result is ``x_i``.

    For floating-point operands,

    - If ``x_i`` is ``+infinity``, the result is ``+infinity``.
    - If ``x_i`` is ``-infinity``, the result is ``-infinity``.
    - If ``x_i`` is ``+0``, the result is ``+0``.
    - If ``x_i`` is ``-0``, the result is ``-0``.
    - If ``x_i`` is ``NaN``, the result is ``NaN``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class argmax[TArray: Array](Protocol):
    """
    Returns the indices of the maximum values along a specified axis.

    When the maximum value occurs multiple times, only the indices corresponding to the first occurrence are returned.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.
    axis: Optional[int]
        axis along which to search. If ``None``, the function must return the index of the maximum value of the flattened array. Default: ``None``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if ``axis`` is ``None``, a zero-dimensional array containing the index of the first occurrence of the maximum value; otherwise, a non-zero-dimensional array containing the indices of the maximum values. The returned array must have be the default array index data type.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class argmin[TArray: Array](Protocol):
    """
    Returns the indices of the minimum values along a specified axis.

    When the minimum value occurs multiple times, only the indices corresponding to the first occurrence are returned.

    .. note::
       For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).

    Parameters
    ----------
    x: array
        input array. Should have a real-valued data type.
    axis: Optional[int]
        axis along which to search. If ``None``, the function must return the index of the minimum value of the flattened array. Default: ``None``.
    keepdims: bool
        if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if ``axis`` is ``None``, a zero-dimensional array containing the index of the first occurrence of the minimum value; otherwise, a non-zero-dimensional array containing the indices of the minimum values. The returned array must have the default array index data type.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class nonzero[TArray: Array](Protocol):
    """
    Returns the indices of the array elements which are non-zero.

    .. note::
       If ``x`` has a complex floating-point data type, non-zero elements are those elements having at least one component (real or imaginary) which is non-zero.

    .. note::
       If ``x`` has a boolean data type, non-zero elements are those elements which are equal to ``True``.

    .. admonition:: Data-dependent output shape
       :class: admonition important

       The shape of the output array for this function depends on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.

    Parameters
    ----------
    x: array
        input array. Must have a positive rank. If ``x`` is zero-dimensional, the function must raise an exception.

    Returns
    -------
    out: Tuple[array, ...]
        a tuple of ``k`` arrays, one for each dimension of ``x`` and each of size ``n`` (where ``n`` is the total number of non-zero elements), containing the indices of the non-zero elements in that dimension. The indices must be returned in row-major, C-style order. The returned array must have the default array index data type.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> tuple[TArray, ...]: ...


@runtime_checkable
class searchsorted[TArray: Array](Protocol):
    """
    Finds the indices into ``x1`` such that, if the corresponding elements in ``x2`` were inserted before the indices, the order of ``x1``, when sorted in ascending order, would be preserved.

    Parameters
    ----------
    x1: array
        input array. Must be a one-dimensional array. Should have a real-valued data type. If ``sorter`` is ``None``, must be sorted in ascending order; otherwise, ``sorter`` must be an array of indices that sort ``x1`` in ascending order.
    x2: array
        array containing search values. Should have a real-valued data type.
    side: Literal['left', 'right']
        argument controlling which index is returned if a value lands exactly on an edge.

        Let ``v`` be an element of ``x2`` given by ``v = x2[j]``, where ``j`` refers to a valid index (see :ref:`indexing`).

        - If ``v`` is less than all elements in ``x1``, then ``out[j]`` must be ``0``.
        - If ``v`` is greater than all elements in ``x1``, then ``out[j]`` must be ``M``, where ``M`` is the number of elements in ``x1``.
        - Otherwise, each returned index ``i = out[j]`` must satisfy an index condition:

          - If ``side == 'left'``, then ``x1[i-1] < v <= x1[i]``.
          - If ``side == 'right'``, then ``x1[i-1] <= v < x1[i]``.

        Default: ``'left'``.
    sorter: Optional[array]
        array of indices that sort ``x1`` in ascending order. The array must have the same shape as ``x1`` and have an integer data type. Default: ``None``.

    Returns
    -------
    out: array
        an array of indices with the same shape as ``x2``. The returned array must have the default array index data type.

    Notes
    -----
    For real-valued floating-point arrays, the sort order of NaNs and signed zeros is unspecified and thus implementation-dependent. Accordingly, when a real-valued floating-point array contains NaNs and signed zeros, what constitutes ascending order may vary among specification-conforming array libraries.

    While behavior for arrays containing NaNs and signed zeros is implementation-dependent, specification-conforming libraries should, however, ensure consistency with ``sort`` and ``argsort`` (i.e., if a value in ``x2`` is inserted into ``x1`` according to the corresponding index in the output array and ``sort`` is invoked on the resultant array, the sorted result should be an array in the same order).

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /, *, side: Literal["left", "right"] = "left", sorter: TArray | None = None) -> TArray: ...


@runtime_checkable
class where[TArray: Array](Protocol):
    """
    Returns elements chosen from ``x1`` or ``x2`` depending on ``condition``.

    Parameters
    ----------
    condition: array
        when ``True``, yield ``x1_i``; otherwise, yield ``x2_i``. Should have a boolean data type. Must be compatible with ``x1`` and ``x2`` (see :ref:`broadcasting`).
    x1: array
        first input array. Must be compatible with ``condition`` and ``x2`` (see :ref:`broadcasting`).
    x2: array
        second input array. Must be compatible with ``condition`` and ``x1`` (see :ref:`broadcasting`).

    Returns
    -------
    out: array
        an array with elements from ``x1`` where ``condition`` is ``True``, and elements from ``x2`` elsewhere. The returned array must have a data type determined by :ref:`type-promotion` rules with the arrays ``x1`` and ``x2``.

    """

    @abstractmethod
    def __call__(self, condition: TArray, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class all[TArray: Array](Protocol):
    """
    Tests whether all input array elements evaluate to ``True`` along a specified axis.

    .. note::
       Positive infinity, negative infinity, and NaN must evaluate to ``True``.

    .. note::
       If ``x`` has a complex floating-point data type, elements having a non-zero component (real or imaginary) must evaluate to ``True``.

    .. note::
       If ``x`` is an empty array or the size of the axis (dimension) along which to evaluate elements is zero, the test result must be ``True``.

    Parameters
    ----------
    x: array
        input array.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which to perform a logical AND reduction. By default, a logical AND reduction must be performed over the entire array. If a tuple of integers, logical AND reductions must be performed over multiple axes. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to perform a reduction by counting backward from the last dimension (where ``-1`` refers to the last dimension). If provided an invalid ``axis``, the function must raise an exception. Default: ``None``.
    keepdims: bool
        If ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if a logical AND reduction was performed over the entire array, the returned array must be a zero-dimensional array containing the test result; otherwise, the returned array must be a non-zero-dimensional array containing the test results. The returned array must have a data type of ``bool``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class any[TArray: Array](Protocol):
    """
    Tests whether any input array element evaluates to ``True`` along a specified axis.

    .. note::
       Positive infinity, negative infinity, and NaN must evaluate to ``True``.

    .. note::
       If ``x`` has a complex floating-point data type, elements having a non-zero component (real or imaginary) must evaluate to ``True``.

    .. note::
       If ``x`` is an empty array or the size of the axis (dimension) along which to evaluate elements is zero, the test result must be ``False``.

    Parameters
    ----------
    x: array
        input array.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis or axes along which to perform a logical OR reduction. By default, a logical OR reduction must be performed over the entire array. If a tuple of integers, logical OR reductions must be performed over multiple axes. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to perform a reduction by counting backward from the last dimension (where ``-1`` refers to the last dimension). If provided an invalid ``axis``, the function must raise an exception. Default: ``None``.
    keepdims: bool
        If ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.

    Returns
    -------
    out: array
        if a logical OR reduction was performed over the entire array, the returned array must be a zero-dimensional array containing the test result; otherwise, the returned array must be a non-zero-dimensional array containing the test results. The returned array must have a data type of ``bool``.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> TArray: ...


@runtime_checkable
class __array_namespace_info__[TDevice](Protocol):
    """
    Returns a namespace with Array API namespace inspection utilities.

    See :ref:`inspection` for a list of inspection APIs.

    Returns
    -------
    out: Info
        An object containing Array API namespace inspection utilities.

    Notes
    -----
    The returned object may be either a namespace or a class, so long as an Array API user can access inspection utilities as follows:

    ::

      info = xp.__array_namespace_info__()
      info.capabilities()
      info.devices()
      info.dtypes()
      info.default_dtypes()
      # ...

    .. versionadded: 2023.12

    """

    @abstractmethod
    def __call__(self, /) -> Info[TDevice,]: ...


@runtime_checkable
class take[TArray: Array](Protocol):
    """
    Returns elements of an array along an axis.

    .. note::
       Conceptually, ``take(x, indices, axis=3)`` is equivalent to ``x[:,:,:,indices,...]``; however, explicit indexing via arrays of indices is not currently supported in this specification due to concerns regarding ``__setitem__`` and array mutation semantics.

    Parameters
    ----------
    x: array
        input array.
    indices: array
        array indices. The array must be one-dimensional and have an integer data type.

        .. note::
           This specification does not require bounds checking. The behavior for out-of-bounds indices is left unspecified.

    axis: Optional[int]
        axis over which to select values. If ``axis`` is negative, the function must determine the axis along which to select values by counting from the last dimension.

        If ``x`` is a one-dimensional array, providing an ``axis`` is optional; however, if ``x`` has more than one dimension, providing an ``axis`` is required.

    Returns
    -------
    out: array
        an array having the same data type as ``x``. The output array must have the same rank (i.e., number of dimensions) as ``x`` and must have the same shape as ``x``, except for the axis specified by ``axis`` whose size must equal the number of elements in ``indices``.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Out-of-bounds behavior is explicitly left unspecified.

    """

    @abstractmethod
    def __call__(self, x: TArray, indices: TArray, /, *, axis: int | None = None) -> TArray: ...


@runtime_checkable
class fft[TArray: Array](Protocol):
    """
    Computes the one-dimensional discrete Fourier transform.

    .. note::
       Applying the one-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifft(fft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (number of elements, axis, and normalization mode).

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    n: Optional[int]
        number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.

        -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.
        -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.
        -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.

        Default: ``None``.
    axis: int
        axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: no normalization.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: normalize by ``1/n``.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axis (dimension) specified by ``axis``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, n: int | None = None, axis: int = -1, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class ifft[TArray: Array](Protocol):
    """
    Computes the one-dimensional inverse discrete Fourier transform.

    .. note::
       Applying the one-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifft(fft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (number of elements, axis, and normalization mode).

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    n: Optional[int]
        number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.

        -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.
        -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.
        -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.

        Default: ``None``.
    axis: int
        axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: normalize by ``1/n``.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: no normalization.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axis (dimension) specified by ``axis``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, n: int | None = None, axis: int = -1, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class fftn[TArray: Array](Protocol):
    """
    Computes the n-dimensional discrete Fourier transform.

    .. note::
       Applying the n-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifftn(fftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (sizes, axes, and normalization mode).

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    s: Optional[Sequence[int]]
        number of elements over which to compute the transform along the axes (dimensions) specified by ``axes``. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``.

        -   If ``s[i]`` is greater than ``M[i]``, axis ``i`` must be zero-padded to size ``s[i]``.
        -   If ``s[i]`` is less than ``M[i]``, axis ``i`` must be trimmed to size ``s[i]``.
        -   If ``s[i]`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` must be used when computing the transform.

        If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.
    axes: Optional[Sequence[int]]
        axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).

        If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.

        If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: no normalization.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: normalize by ``1/n``.

        where ``n = prod(s)`` is the logical FFT size.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axes (dimensions) specified by ``axes``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axes specified by ``axes`` which must have size ``s[i]``.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, s: Sequence[int] | None = None, axes: Sequence[int] | None = None, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class ifftn[TArray: Array](Protocol):
    """
    Computes the n-dimensional inverse discrete Fourier transform.

    .. note::
       Applying the n-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifftn(fftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (sizes, axes, and normalization mode).

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    s: Optional[Sequence[int]]
        number of elements over which to compute the transform along the axes (dimensions) specified by ``axes``. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``.

        -   If ``s[i]`` is greater than ``M[i]``, axis ``i`` must be zero-padded to size ``s[i]``.
        -   If ``s[i]`` is less than ``M[i]``, axis ``i`` must be trimmed to size ``s[i]``.
        -   If ``s[i]`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` must be used when computing the transform.

        If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.
    axes: Optional[Sequence[int]]
        axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).

        If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.

        If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.
    norm: Literal['backward', 'ortho', 'forward']
        specify the normalization mode. Should be one of the following modes:

        - ``'backward'``: normalize by ``1/n``.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: no normalization.

        where ``n = prod(s)`` is the logical FFT size.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axes (dimensions) specified by ``axes``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axes specified by ``axes`` which must have size ``s[i]``.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, s: Sequence[int] | None = None, axes: Sequence[int] | None = None, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class rfft[TArray: Array](Protocol):
    """
    Computes the one-dimensional discrete Fourier transform for real-valued input.

    .. note::
       Applying the one-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfft(rfft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axis and normalization mode) and consistent values for the number of elements over which to compute the transforms.

    Parameters
    ----------
    x: array
        input array. Must have a real-valued floating-point data type.
    n: Optional[int]
        number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.

        -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.
        -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.
        -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.

        Default: ``None``.
    axis: int
        axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: no normalization.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: normalize by ``1/n``.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a complex floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``float64``, then the returned array must have a ``complex128`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n//2 + 1``.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, n: int | None = None, axis: int = -1, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class irfft[TArray: Array](Protocol):
    """
    Computes the one-dimensional inverse of ``rfft`` for complex-valued input.

    .. note::
       Applying the one-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfft(rfft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axis and normalization mode) and consistent values for the number of elements over which to compute the transforms.

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    n: Optional[int]
        number of elements along the transformed axis (dimension) specified by ``axis`` in the **output array**. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``2*(M-1)``.

        -   If ``n//2+1`` is greater than ``M``, the axis of the input array specified by ``axis`` must be zero-padded to size ``n//2+1``.
        -   If ``n//2+1`` is less than ``M``, the axis of the input array specified by ``axis`` must be trimmed to size ``n//2+1``.
        -   If ``n//2+1`` equals ``M``, all elements along the axis of the input array specified by ``axis`` must be used when computing the transform.

        Default: ``None``.
    axis: int
        axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: normalize by ``1/n``.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: no normalization.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.

    Notes
    -----
    -   In order to return an array having an odd number of elements along the transformed axis, the function must be provided an odd integer for ``n``.

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the output array have a real-valued floating-point data type having the same precision as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, n: int | None = None, axis: int = -1, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class rfftn[TArray: Array](Protocol):
    """
    Computes the n-dimensional discrete Fourier transform for real-valued input.

    .. note::
       Applying the n-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfftn(rfftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axes and normalization mode) and consistent sizes.

    Parameters
    ----------
    x: array
        input array. Must have a real-valued floating-point data type.
    s: Optional[Sequence[int]]
        number of elements over which to compute the transform along axes (dimensions) specified by ``axes``. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``.

        -   If ``s[i]`` is greater than ``M[i]``, axis ``i`` must be zero-padded to size ``s[i]``.
        -   If ``s[i]`` is less than ``M[i]``, axis ``i`` must be trimmed to size ``s[i]``.
        -   If ``s[i]`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` must be used when computing the transform.

        If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.
    axes: Optional[Sequence[int]]
        axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).

        If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.

        If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: no normalization.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: normalize by ``1/n``.

        where ``n = prod(s)``, the logical FFT size.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axes (dimension) specified by ``axes``. The returned array must have a complex floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``float64``, then the returned array must have a ``complex128`` data type). The returned array must have the same shape as ``x``, except for the last transformed axis which must have size ``s[-1]//2 + 1`` and the remaining transformed axes which must have size ``s[i]``.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, s: Sequence[int] | None = None, axes: Sequence[int] | None = None, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class irfftn[TArray: Array](Protocol):
    """
    Computes the n-dimensional inverse of ``rfftn`` for complex-valued input.

    .. note::
       Applying the n-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfftn(rfftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axes and normalization mode) and consistent sizes.

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    s: Optional[Sequence[int]]
        number of elements along the transformed axes (dimensions) specified by ``axes`` in the **output array**. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``, except for the last transformed axis in which ``s[i]`` equals ``2*(M[i]-1)``. For each ``i``, let ``n`` equal ``s[i]``, except for the last transformed axis in which ``n`` equals ``s[i]//2+1``.

        -   If ``n`` is greater than ``M[i]``, axis ``i`` of the input array must be zero-padded to size ``n``.
        -   If ``n`` is less than ``M[i]``, axis ``i`` of the input array must be trimmed to size ``n``.
        -   If ``n`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` of the input array must be used when computing the transform.

        If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.
    axes: Optional[Sequence[int]]
        axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).

        If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.

        If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: normalize by ``1/n``.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: no normalization.

        where ``n = prod(s)`` is the logical FFT size.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axes (dimension) specified by ``axes``. The returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type). The returned array must have the same shape as ``x``, except for the transformed axes which must have size ``s[i]``.

    Notes
    -----
    -   In order to return an array having an odd number of elements along the last transformed axis, the function must be provided an odd integer for ``s[-1]``.

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the output array have a real-valued floating-point data type having the same precision as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, s: Sequence[int] | None = None, axes: Sequence[int] | None = None, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class hfft[TArray: Array](Protocol):
    """
    Computes the one-dimensional discrete Fourier transform of a signal with Hermitian symmetry.

    Parameters
    ----------
    x: array
        input array. Should have a complex floating-point data type.
    n: Optional[int]
        number of elements along the transformed axis (dimension) specified by ``axis`` in the **output array**. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``2*(M-1)``.

        -   If ``n//2+1`` is greater than ``M``, the axis of the input array specified by ``axis`` must be zero-padded to length ``n//2+1``.
        -   If ``n//2+1`` is less than ``M``, the axis of the input array specified by ``axis`` must be trimmed to size ``n//2+1``.
        -   If ``n//2+1`` equals ``M``, all elements along the axis of the input array specified by ``axis`` must be used when computing the transform.

        Default: ``None``.
    axis: int
        axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: no normalization.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: normalize by ``1/n``.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the input array to have a complex floating-point data type and required that the output array have a real-valued data type having the same precision as the input array.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, n: int | None = None, axis: int = -1, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class ihfft[TArray: Array](Protocol):
    """
    Computes the one-dimensional inverse discrete Fourier transform of a signal with Hermitian symmetry.

    Parameters
    ----------
    x: array
        input array. Must have a real-valued floating-point data type.
    n: Optional[int]
        number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.

        -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.
        -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.
        -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.

        Default: ``None``.
    axis: int
        axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.
    norm: Literal['backward', 'ortho', 'forward']
        normalization mode. Should be one of the following modes:

        - ``'backward'``: normalize by ``1/n``.
        - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).
        - ``'forward'``: no normalization.

        Default: ``'backward'``.

    Returns
    -------
    out: array
        an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a complex floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``float64``, then the returned array must have a ``complex128`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n//2 + 1``.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, n: int | None = None, axis: int = -1, norm: Literal["backward", "ortho", "forward"] = "backward") -> TArray: ...


@runtime_checkable
class fftfreq[TArray: Array, TDevice](Protocol):
    """
    Computes the discrete Fourier transform sample frequencies.

    For a Fourier transform of length ``n`` and length unit of ``d``, the frequencies are described as:

    .. code-block::

      f = [0, 1, ..., n/2-1, -n/2, ..., -1] / (d*n)        # if n is even
      f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)  # if n is odd

    Parameters
    ----------
    n: int
        window length.
    d: float
        sample spacing between individual samples of the Fourier transform input. Default: ``1.0``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array of shape ``(n,)`` containing the sample frequencies. The returned array must have the default real-valued floating-point data type.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the output array have the default real-valued floating-point data type.

    """

    @abstractmethod
    def __call__(self, n: int, /, *, d: float = 1.0, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class rfftfreq[TArray: Array, TDevice](Protocol):
    """
    Computes the discrete Fourier transform sample frequencies (for ``rfft`` and ``irfft``).

    For a Fourier transform of length ``n`` and length unit of ``d``, the frequencies are described as:

    .. code-block::

      f = [0, 1, ...,     n/2-1,     n/2] / (d*n)  # if n is even
      f = [0, 1, ..., (n-1)/2-1, (n-1)/2] / (d*n)  # if n is odd

    The Nyquist frequency component is considered to be positive.

    Parameters
    ----------
    n: int
        window length.
    d: float
        sample spacing between individual samples of the Fourier transform input. Default: ``1.0``.
    device: Optional[device]
        device on which to place the created array. Default: ``None``.

    Returns
    -------
    out: array
        an array of shape ``(n//2+1,)`` containing the sample frequencies. The returned array must have the default real-valued floating-point data type.

    Notes
    -----

    .. versionadded:: 2022.12

    .. versionchanged:: 2023.12
       Required the output array have the default real-valued floating-point data type.

    """

    @abstractmethod
    def __call__(self, n: int, /, *, d: float = 1.0, device: TDevice | None = None) -> TArray: ...


@runtime_checkable
class fftshift[TArray: Array](Protocol):
    """
    Shifts the zero-frequency component to the center of the spectrum.

    This function swaps half-spaces for all axes (dimensions) specified by ``axes``.

    .. note::
       ``out[0]`` is the Nyquist component only if the length of the input is even.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.
    axes: Optional[Union[int, Sequence[int]]]
        axes over which to shift. If ``None``, the function must shift all axes. Default: ``None``.

        If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.

    Returns
    -------
    out: array
        the shifted array. The returned array must have the same data type and shape as ``x``.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axes: int | Sequence[int] | None = None) -> TArray: ...


@runtime_checkable
class ifftshift[TArray: Array](Protocol):
    """
    Inverse of ``fftshift``.

    .. note::
       Although identical for even-length ``x``, ``fftshift`` and ``ifftshift`` differ by one sample for odd-length ``x``.

    Parameters
    ----------
    x: array
        input array. Should have a floating-point data type.
    axes: Optional[Union[int, Sequence[int]]]
        axes over which to perform the inverse shift. If ``None``, the function must shift all axes. Default: ``None``.

        If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.

    Returns
    -------
    out: array
        the shifted array. The returned array must have the same data type and shape as ``x``.

    Notes
    -----

    .. versionadded:: 2022.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axes: int | Sequence[int] | None = None) -> TArray: ...


@runtime_checkable
class matmul[TArray: Array](Protocol):
    """
    Computes the matrix product.

    .. note::
       The ``matmul`` function must implement the same semantics as the built-in ``@`` operator (see `PEP 465 <https://www.python.org/dev/peps/pep-0465>`_).

    Parameters
    ----------
    x1: array
        first input array. Should have a numeric data type. Must have at least one dimension. If ``x1`` is one-dimensional having shape ``(M,)`` and ``x2`` has more than one dimension, ``x1`` must be promoted to a two-dimensional array by prepending ``1`` to its dimensions (i.e., must have shape ``(1, M)``). After matrix multiplication, the prepended dimensions in the returned array must be removed. If ``x1`` has more than one dimension (including after vector-to-matrix promotion), ``shape(x1)[:-2]`` must be compatible with ``shape(x2)[:-2]`` (after vector-to-matrix promotion) (see :ref:`broadcasting`). If ``x1`` has shape ``(..., M, K)``, the innermost two dimensions form matrices on which to perform matrix multiplication.
    x2: array
        second input array. Should have a numeric data type. Must have at least one dimension. If ``x2`` is one-dimensional having shape ``(N,)`` and ``x1`` has more than one dimension, ``x2`` must be promoted to a two-dimensional array by appending ``1`` to its dimensions (i.e., must have shape ``(N, 1)``). After matrix multiplication, the appended dimensions in the returned array must be removed. If ``x2`` has more than one dimension (including after vector-to-matrix promotion), ``shape(x2)[:-2]`` must be compatible with ``shape(x1)[:-2]`` (after vector-to-matrix promotion) (see :ref:`broadcasting`). If ``x2`` has shape ``(..., K, N)``, the innermost two dimensions form matrices on which to perform matrix multiplication.


    .. note::
       If either ``x1`` or ``x2`` has a complex floating-point data type, neither argument must be complex-conjugated or transposed. If conjugation and/or transposition is desired, these operations should be explicitly performed prior to computing the matrix product.

    Returns
    -------
    out: array
        -   if both ``x1`` and ``x2`` are one-dimensional arrays having shape ``(N,)``, a zero-dimensional array containing the inner product as its only element.
        -   if ``x1`` is a two-dimensional array having shape ``(M, K)`` and ``x2`` is a two-dimensional array having shape ``(K, N)``, a two-dimensional array containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ and having shape ``(M, N)``.
        -   if ``x1`` is a one-dimensional array having shape ``(K,)`` and ``x2`` is an array having shape ``(..., K, N)``, an array having shape ``(..., N)`` (i.e., prepended dimensions during vector-to-matrix promotion must be removed) and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_.
        -   if ``x1`` is an array having shape ``(..., M, K)`` and ``x2`` is a one-dimensional array having shape ``(K,)``, an array having shape ``(..., M)`` (i.e., appended dimensions during vector-to-matrix promotion must be removed) and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_.
        -   if ``x1`` is a two-dimensional array having shape ``(M, K)`` and ``x2`` is an array having shape ``(..., K, N)``, an array having shape ``(..., M, N)`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.
        -   if ``x1`` is an array having shape ``(..., M, K)`` and ``x2`` is a two-dimensional array having shape ``(K, N)``, an array having shape ``(..., M, N)`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.
        -   if either ``x1`` or ``x2`` has more than two dimensions, an array having a shape determined by :ref:`broadcasting` ``shape(x1)[:-2]`` against ``shape(x2)[:-2]`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.

        The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    **Raises**

    -   if either ``x1`` or ``x2`` is a zero-dimensional array.
    -   if ``x1`` is a one-dimensional array having shape ``(K,)``, ``x2`` is a one-dimensional array having shape ``(L,)``, and ``K != L``.
    -   if ``x1`` is a one-dimensional array having shape ``(K,)``, ``x2`` is an array having shape ``(..., L, N)``, and ``K != L``.
    -   if ``x1`` is an array having shape ``(..., M, K)``, ``x2`` is a one-dimensional array having shape ``(L,)``, and ``K != L``.
    -   if ``x1`` is an array having shape ``(..., M, K)``, ``x2`` is an array having shape ``(..., L, N)``, and ``K != L``.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /) -> TArray: ...


@runtime_checkable
class matrix_transpose[TArray: Array](Protocol):
    """
    Transposes a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x: array
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.

    Returns
    -------
    out: array
        an array containing the transpose for each matrix and having shape ``(..., N, M)``. The returned array must have the same data type as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class tensordot[TArray: Array](Protocol):
    """
    Returns a tensor contraction of ``x1`` and ``x2`` over specific axes.

    .. note::
       The ``tensordot`` function corresponds to the generalized matrix product.

    Parameters
    ----------
    x1: array
        first input array. Should have a numeric data type.
    x2: array
        second input array. Should have a numeric data type. Corresponding contracted axes of ``x1`` and ``x2`` must be equal.

        .. note::
           Contracted axes (dimensions) must not be broadcasted.

    axes: Union[int, Tuple[Sequence[int], Sequence[int]]]
        number of axes (dimensions) to contract or explicit sequences of axis (dimension) indices for ``x1`` and ``x2``, respectively.

        If ``axes`` is an ``int`` equal to ``N``, then contraction must be performed over the last ``N`` axes of ``x1`` and the first ``N`` axes of ``x2`` in order. The size of each corresponding axis (dimension) must match. Must be nonnegative.

        -   If ``N`` equals ``0``, the result is the tensor (outer) product.
        -   If ``N`` equals ``1``, the result is the tensor dot product.
        -   If ``N`` equals ``2``, the result is the tensor double contraction (default).

        If ``axes`` is a tuple of two sequences ``(x1_axes, x2_axes)``, the first sequence must apply to ``x1`` and the second sequence to ``x2``. Both sequences must have the same length. Each axis (dimension) ``x1_axes[i]`` for ``x1`` must have the same size as the respective axis (dimension) ``x2_axes[i]`` for ``x2``. Each index referred to in a sequence must be unique. If ``x1`` has rank (i.e, number of dimensions) ``N``, a valid ``x1`` axis must reside on the half-open interval ``[-N, N)``. If ``x2`` has rank ``M``, a valid ``x2`` axis must reside on the half-open interval ``[-M, M)``.


    .. note::
       If either ``x1`` or ``x2`` has a complex floating-point data type, neither argument must be complex-conjugated or transposed. If conjugation and/or transposition is desired, these operations should be explicitly performed prior to computing the generalized matrix product.

    Returns
    -------
    out: array
        an array containing the tensor contraction whose shape consists of the non-contracted axes (dimensions) of the first array ``x1``, followed by the non-contracted axes (dimensions) of the second array ``x2``. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Allow negative axes.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /, *, axes: int | tuple[Sequence[int], Sequence[int]] = 2) -> TArray: ...


@runtime_checkable
class vecdot[TArray: Array](Protocol):
    r"""
    Computes the (vector) dot product of two arrays.

    Let :math:`\\mathbf{a}` be a vector in ``x1`` and :math:`\\mathbf{b}` be a corresponding vector in ``x2``. The dot product is defined as

    .. math::
       \\mathbf{a} \\cdot \\mathbf{b} = \\sum_{i=0}^{n-1} \\overline{a_i}b_i

    over the dimension specified by ``axis`` and where :math:`n` is the dimension size and :math:`\\overline{a_i}` denotes the complex conjugate if :math:`a_i` is complex and the identity if :math:`a_i` is real-valued.

    Parameters
    ----------
    x1: array
        first input array. Should have a floating-point data type.
    x2: array
        second input array. Must be compatible with ``x1`` for all non-contracted axes (see :ref:`broadcasting`). The size of the axis over which to compute the dot product must be the same size as the respective axis in ``x1``. Should have a floating-point data type.

        .. note::
           The contracted axis (dimension) must not be broadcasted.

    axis: int
        the axis (dimension) of ``x1`` and ``x2`` containing the vectors for which to compute the dot product. Should be an integer on the interval ``[-N, -1]``, where ``N`` is ``min(x1.ndim, x2.ndim)``. The function must determine the axis along which to compute the dot product by counting backward from the last dimension (where ``-1`` refers to the last dimension). By default, the function must compute the dot product over the last axis. Default: ``-1``.

    Returns
    -------
    out: array
        if ``x1`` and ``x2`` are both one-dimensional arrays, a zero-dimensional containing the dot product; otherwise, a non-zero-dimensional array containing the dot products and having rank ``N-1``, where ``N`` is the rank (number of dimensions) of the shape determined according to :ref:`broadcasting` along the non-contracted axes. The returned array must have a data type determined by :ref:`type-promotion`.

    Notes
    -----
    **Raises**

    -   if the size of the axis over which to compute the dot product is not the same (before broadcasting) for both ``x1`` and ``x2``.

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Restricted ``axis`` to only negative integers.

    """

    @abstractmethod
    def __call__(self, x1: TArray, x2: TArray, /, *, axis: int = -1) -> TArray: ...


@runtime_checkable
class broadcast_arrays[TArray: Array](Protocol):
    """
    Broadcasts one or more arrays against one another.

    Parameters
    ----------
    arrays: array
        an arbitrary number of to-be broadcasted arrays.

    Returns
    -------
    out: List[array]
        a list of broadcasted arrays. Each array must have the same shape. Each array must have the same dtype as its corresponding input array.

    """

    @abstractmethod
    def __call__(self, /, *arrays: TArray) -> list[TArray]: ...


@runtime_checkable
class broadcast_to[TArray: Array](Protocol):
    """
    Broadcasts an array to a specified shape.

    Parameters
    ----------
    x: array
        array to broadcast.
    shape: Tuple[int, ...]
        array shape. Must be compatible with ``x`` (see :ref:`broadcasting`). If the array is incompatible with the specified shape, the function should raise an exception.

    Returns
    -------
    out: array
        an array having a specified shape. Must have the same data type as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, shape: tuple[int, ...]) -> TArray: ...


@runtime_checkable
class concat[TArray: Array](Protocol):
    """
    Joins a sequence of arrays along an existing axis.

    Parameters
    ----------
    arrays: Union[Tuple[array, ...], List[array]]
        input arrays to join. The arrays must have the same shape, except in the dimension specified by ``axis``.
    axis: Optional[int]
        axis along which the arrays will be joined. If ``axis`` is ``None``, arrays must be flattened before concatenation. If ``axis`` is negative, the function must determine the axis along which to join by counting from the last dimension. Default: ``0``.

    Returns
    -------
    out: array
        an output array containing the concatenated values. If the input arrays have different data types, normal :ref:`type-promotion` must apply. If the input arrays have the same data type, the output array must have the same data type as the input arrays.

        .. note::
           This specification leaves type promotion between data type families (i.e., ``intxx`` and ``floatxx``) unspecified.

    """

    @abstractmethod
    def __call__(self, arrays: tuple[TArray, ...] | list[TArray], /, *, axis: int | None = 0) -> TArray: ...


@runtime_checkable
class expand_dims[TArray: Array](Protocol):
    """
    Expands the shape of an array by inserting a new axis (dimension) of size one at the position specified by ``axis``.

    Parameters
    ----------
    x: array
        input array.
    axis: int
        axis position (zero-based). If ``x`` has rank (i.e, number of dimensions) ``N``, a valid ``axis`` must reside on the closed-interval ``[-N-1, N]``. If provided a negative ``axis``, the axis position at which to insert a singleton dimension must be computed as ``N + axis + 1``. Hence, if provided ``-1``, the resolved axis position must be ``N`` (i.e., a singleton dimension must be appended to the input array ``x``). If provided ``-N-1``, the resolved axis position must be ``0`` (i.e., a singleton dimension must be prepended to the input array ``x``).

    Returns
    -------
    out: array
        an expanded output array having the same data type as ``x``.

    Raises
    ------
    IndexError
        If provided an invalid ``axis`` position, an ``IndexError`` should be raised.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int = 0) -> TArray: ...


@runtime_checkable
class flip[TArray: Array](Protocol):
    """
    Reverses the order of elements in an array along the given axis. The shape of the array must be preserved.

    Parameters
    ----------
    x: array
        input array.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis (or axes) along which to flip. If ``axis`` is ``None``, the function must flip all input array axes. If ``axis`` is negative, the function must count from the last dimension. If provided more than one axis, the function must flip only the specified axes. Default: ``None``.

    Returns
    -------
    out: array
        an output array having the same data type and shape as ``x`` and whose elements, relative to ``x``, are reordered.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int | tuple[int, ...] | None = None) -> TArray: ...


@runtime_checkable
class moveaxis[TArray: Array](Protocol):
    """
    Moves array axes (dimensions) to new positions, while leaving other axes in their original positions.

    Parameters
    ----------
    x: array
        input array.
    source: Union[int, Tuple[int, ...]]
        Axes to move. Provided axes must be unique. If ``x`` has rank (i.e, number of dimensions) ``N``, a valid axis must reside on the half-open interval ``[-N, N)``.
    destination: Union[int, Tuple[int, ...]]
        indices defining the desired positions for each respective ``source`` axis index. Provided indices must be unique. If ``x`` has rank (i.e, number of dimensions) ``N``, a valid axis must reside on the half-open interval ``[-N, N)``.

    Returns
    -------
    out: array
        an array containing reordered axes. The returned array must have the same data type as ``x``.

    Notes
    -----

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, source: int | tuple[int, ...], destination: int | tuple[int, ...], /) -> TArray: ...


@runtime_checkable
class permute_dims[TArray: Array](Protocol):
    """
    Permutes the axes (dimensions) of an array ``x``.

    Parameters
    ----------
    x: array
        input array.
    axes: Tuple[int, ...]
        tuple containing a permutation of ``(0, 1, ..., N-1)`` where ``N`` is the number of axes (dimensions) of ``x``.

    Returns
    -------
    out: array
        an array containing the axes permutation. The returned array must have the same data type as ``x``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, axes: tuple[int, ...]) -> TArray: ...


@runtime_checkable
class repeat[TArray: Array](Protocol):
    """
    Repeats each element of an array a specified number of times on a per-element basis.

    .. admonition:: Data-dependent output shape
        :class: important

        When ``repeats`` is an array, the shape of the output array for this function depends on the data values in the ``repeats`` array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing the values in ``repeats``. Accordingly, such libraries may choose to omit support for ``repeats`` arrays; however, conforming implementations must support providing a literal ``int``. See :ref:`data-dependent-output-shapes` section for more details.

    Parameters
    ----------
    x: array
        input array containing elements to repeat.
    repeats: Union[int, array]
        the number of repetitions for each element.

        If ``axis`` is ``None``, let ``N = prod(x.shape)`` and

        -   if ``repeats`` is an array, ``repeats`` must be broadcast compatible with the shape ``(N,)`` (i.e., be a one-dimensional array having shape ``(1,)`` or ``(N,)``).
        -   if ``repeats`` is an integer, ``repeats`` must be broadcasted to the shape `(N,)`.

        If ``axis`` is not ``None``, let ``M = x.shape[axis]`` and

        -   if ``repeats`` is an array, ``repeats`` must be broadcast compatible with the shape ``(M,)`` (i.e., be a one-dimensional array having shape ``(1,)`` or ``(M,)``).
        -   if ``repeats`` is an integer, ``repeats`` must be broadcasted to the shape ``(M,)``.

        If ``repeats`` is an array, the array must have an integer data type.

        .. note::
           For specification-conforming array libraries supporting hardware acceleration, providing an array for ``repeats`` may cause device synchronization due to an unknown output shape. For those array libraries where synchronization concerns are applicable, conforming array libraries are advised to include a warning in their documentation regarding potential performance degradation when ``repeats`` is an array.

    axis: Optional[int]
        the axis (dimension) along which to repeat elements. If ``axis`` is `None`, the function must flatten the input array ``x`` and then repeat elements of the flattened input array and return the result as a one-dimensional output array. A flattened input array must be flattened in row-major, C-style order. Default: ``None``.

    Returns
    -------
    out: array
        an output array containing repeated elements. The returned array must have the same data type as ``x``. If ``axis`` is ``None``, the returned array must be a one-dimensional array; otherwise, the returned array must have the same shape as ``x``, except for the axis (dimension) along which elements were repeated.

    Notes
    -----

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, repeats: int | TArray, /, *, axis: int | None = None) -> TArray: ...


@runtime_checkable
class reshape[TArray: Array](Protocol):
    """
    Reshapes an array without changing its data.

    Parameters
    ----------
    x: array
        input array to reshape.
    shape: Tuple[int, ...]
        a new shape compatible with the original shape. One shape dimension is allowed to be ``-1``. When a shape dimension is ``-1``, the corresponding output array shape dimension must be inferred from the length of the array and the remaining dimensions.
    copy: Optional[bool]
        whether or not to copy the input array. If ``True``, the function must always copy. If ``False``, the function must never copy. If ``None``, the function must avoid copying, if possible, and may copy otherwise. Default: ``None``.

    Returns
    -------
    out: array
        an output array having the same data type and elements as ``x``.

    Raises
    ------
    ValueError
        If ``copy=False`` and a copy would be necessary, a ``ValueError``
        should be raised.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, shape: tuple[int, ...], *, copy: bool | None = None) -> TArray: ...


@runtime_checkable
class roll[TArray: Array](Protocol):
    """
    Rolls array elements along a specified axis. Array elements that roll beyond the last position are re-introduced at the first position. Array elements that roll beyond the first position are re-introduced at the last position.

    Parameters
    ----------
    x: array
        input array.
    shift: Union[int, Tuple[int, ...]]
        number of places by which the elements are shifted. If ``shift`` is a tuple, then ``axis`` must be a tuple of the same size, and each of the given axes must be shifted by the corresponding element in ``shift``. If ``shift`` is an ``int`` and ``axis`` a tuple, then the same ``shift`` must be used for all specified axes. If a shift is positive, then array elements must be shifted positively (toward larger indices) along the dimension of ``axis``. If a shift is negative, then array elements must be shifted negatively (toward smaller indices) along the dimension of ``axis``.
    axis: Optional[Union[int, Tuple[int, ...]]]
        axis (or axes) along which elements to shift. If ``axis`` is ``None``, the array must be flattened, shifted, and then restored to its original shape. Default: ``None``.

    Returns
    -------
    out: array
        an output array having the same data type as ``x`` and whose elements, relative to ``x``, are shifted.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, shift: int | tuple[int, ...], *, axis: int | tuple[int, ...] | None = None) -> TArray: ...


@runtime_checkable
class squeeze[TArray: Array](Protocol):
    """
    Removes singleton dimensions (axes) from ``x``.

    Parameters
    ----------
    x: array
        input array.
    axis: Union[int, Tuple[int, ...]]
        axis (or axes) to squeeze.

    Returns
    -------
    out: array
        an output array having the same data type and elements as ``x``.

    Raises
    ------
    ValueError
        If a specified axis has a size greater than one (i.e., it is not a
        singleton dimension), a ``ValueError`` should be raised.

    """

    @abstractmethod
    def __call__(self, x: TArray, /, axis: int | tuple[int, ...]) -> TArray: ...


@runtime_checkable
class stack[TArray: Array](Protocol):
    """
    Joins a sequence of arrays along a new axis.

    Parameters
    ----------
    arrays: Union[Tuple[array, ...], List[array]]
        input arrays to join. Each array must have the same shape.
    axis: int
        axis along which the arrays will be joined. Providing an ``axis`` specifies the index of the new axis in the dimensions of the result. For example, if ``axis`` is ``0``, the new axis will be the first dimension and the output array will have shape ``(N, A, B, C)``; if ``axis`` is ``1``, the new axis will be the second dimension and the output array will have shape ``(A, N, B, C)``; and, if ``axis`` is ``-1``, the new axis will be the last dimension and the output array will have shape ``(A, B, C, N)``. A valid ``axis`` must be on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If provided an ``axis`` outside of the required interval, the function must raise an exception. Default: ``0``.

    Returns
    -------
    out: array
        an output array having rank ``N+1``, where ``N`` is the rank (number of dimensions) of ``x``. If the input arrays have different data types, normal :ref:`type-promotion` must apply. If the input arrays have the same data type, the output array must have the same data type as the input arrays.

        .. note::
           This specification leaves type promotion between data type families (i.e., ``intxx`` and ``floatxx``) unspecified.

    """

    @abstractmethod
    def __call__(self, arrays: tuple[TArray, ...] | list[TArray], /, *, axis: int = 0) -> TArray: ...


@runtime_checkable
class tile[TArray: Array](Protocol):
    """
    Constructs an array by tiling an input array.

    Parameters
    ----------
    x: array
        input array.
    repetitions: Tuple[int, ...]
        number of repetitions along each axis (dimension).

        Let ``N = len(x.shape)`` and ``M = len(repetitions)``.

        If ``N > M``, the function must prepend ones until all axes (dimensions) are specified (e.g., if ``x`` has shape ``(8,6,4,2)`` and ``repetitions`` is the tuple ``(3,3)``, then ``repetitions`` must be treated as ``(1,1,3,3)``).

        If ``N < M``, the function must prepend singleton axes (dimensions) to ``x`` until ``x`` has as many axes (dimensions) as ``repetitions`` specifies (e.g., if ``x`` has shape ``(4,2)`` and ``repetitions`` is the tuple ``(3,3,3,3)``, then ``x`` must be treated as if it has shape ``(1,1,4,2)``).

    Returns
    -------
    out: array
        a tiled output array. The returned array must have the same data type as ``x`` and must have a rank (i.e., number of dimensions) equal to ``max(N, M)``. If ``S`` is the shape of the tiled array after prepending singleton dimensions (if necessary) and ``r`` is the tuple of repetitions after prepending ones (if necessary), then the number of elements along each axis (dimension) must satisfy ``S[i]*r[i]``, where ``i`` refers to the ``i`` th axis (dimension).

    Notes
    -----

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, repetitions: tuple[int, ...], /) -> TArray: ...


@runtime_checkable
class unstack[TArray: Array](Protocol):
    """
    Splits an array into a sequence of arrays along the given axis.

    Parameters
    ----------
    x: array
        input array.
    axis: int
        axis along which the array will be split. A valid ``axis`` must be on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If provided an ``axis`` outside of the required interval, the function must raise an exception. Default: ``0``.

    Returns
    -------
    out: Tuple[array, ...]
        tuple of slices along the given dimension. All the arrays have the same shape.

    Notes
    -----

    .. versionadded:: 2023.12

    """

    @abstractmethod
    def __call__(self, x: TArray, /, *, axis: int = 0) -> tuple[TArray, ...]: ...


@runtime_checkable
class unique_all[TArray: Array](Protocol):
    """
    Returns the unique elements of an input array ``x``, the first occurring indices for each unique element in ``x``, the indices from the set of unique elements that reconstruct ``x``, and the corresponding counts for each unique element in ``x``.

    .. admonition:: Data-dependent output shape
        :class: important

        The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.

    .. note::
       Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.

       -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.
       -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.
       -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).

       As signed zeros are not distinct, using ``inverse_indices`` to reconstruct the input array is not guaranteed to return an array having the exact same values.

       Each ``nan`` value and each complex floating-point value having a ``nan`` component should have a count of one, while the counts for signed zeros should be aggregated as a single count.

    Parameters
    ----------
    x: array
        input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.

    Returns
    -------
    out: Tuple[array, array, array, array]
        a namedtuple ``(values, indices, inverse_indices, counts)`` whose

        - first element must have the field name ``values`` and must be a one-dimensional array containing the unique elements of ``x``. The array must have the same data type as ``x``.
        - second element must have the field name ``indices`` and must be an array containing the indices (first occurrences) of a flattened ``x`` that result in ``values``. The array must have the same shape as ``values`` and must have the default array index data type.
        - third element must have the field name ``inverse_indices`` and must be an array containing the indices of ``values`` that reconstruct ``x``. The array must have the same shape as ``x`` and must have the default array index data type.
        - fourth element must have the field name ``counts`` and must be an array containing the number of times each unique element occurs in ``x``. The order of the returned counts must match the order of ``values``, such that a specific element in ``counts`` corresponds to the respective unique element in ``values``. The returned array must have same shape as ``values`` and must have the default array index data type.

        .. note::
           The order of unique elements is not specified and may vary between implementations.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Clarified flattening behavior and required the order of ``counts`` match the order of ``values``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> tuple[TArray, TArray, TArray, TArray]: ...


@runtime_checkable
class unique_counts[TArray: Array](Protocol):
    """
    Returns the unique elements of an input array ``x`` and the corresponding counts for each unique element in ``x``.

    .. admonition:: Data-dependent output shape
        :class: important

        The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.

    .. note::
       Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.

       -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.
       -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.
       -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).

       Each ``nan`` value and each complex floating-point value having a ``nan`` component should have a count of one, while the counts for signed zeros should be aggregated as a single count.

    Parameters
    ----------
    x: array
        input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.

    Returns
    -------
    out: Tuple[array, array]
        a namedtuple `(values, counts)` whose

        -   first element must have the field name ``values`` and must be a one-dimensional array containing the unique elements of ``x``. The array must have the same data type as ``x``.
        -   second element must have the field name `counts` and must be an array containing the number of times each unique element occurs in ``x``. The order of the returned counts must match the order of ``values``, such that a specific element in ``counts`` corresponds to the respective unique element in ``values``. The returned array must have same shape as ``values`` and must have the default array index data type.

        .. note::
           The order of unique elements is not specified and may vary between implementations.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Clarified flattening behavior and required the order of ``counts`` match the order of ``values``.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> tuple[TArray, TArray]: ...


@runtime_checkable
class unique_inverse[TArray: Array](Protocol):
    """
    Returns the unique elements of an input array ``x`` and the indices from the set of unique elements that reconstruct ``x``.

    .. admonition:: Data-dependent output shape
        :class: important

        The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.

    .. note::
       Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.

       -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.
       -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.
       -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).

       As signed zeros are not distinct, using ``inverse_indices`` to reconstruct the input array is not guaranteed to return an array having the exact same values.

    Parameters
    ----------
    x: array
        input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.

    Returns
    -------
    out: Tuple[array, array]
        a namedtuple ``(values, inverse_indices)`` whose

        -   first element must have the field name ``values`` and must be a one-dimensional array containing the unique elements of ``x``. The array must have the same data type as ``x``.
        -   second element must have the field name ``inverse_indices`` and must be an array containing the indices of ``values`` that reconstruct ``x``. The array must have the same shape as ``x`` and have the default array index data type.

        .. note::
           The order of unique elements is not specified and may vary between implementations.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Clarified flattening behavior.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> tuple[TArray, TArray]: ...


@runtime_checkable
class unique_values[TArray: Array](Protocol):
    """
    Returns the unique elements of an input array ``x``.

    .. admonition:: Data-dependent output shape
        :class: important

        The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.

    .. note::
       Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.

       -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.
       -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.
       -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).

    Parameters
    ----------
    x: array
        input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.

    Returns
    -------
    out: array
        a one-dimensional array containing the set of unique elements in ``x``. The returned array must have the same data type as ``x``.

        .. note::
           The order of unique elements is not specified and may vary between implementations.

    Notes
    -----

    .. versionchanged:: 2022.12
       Added complex data type support.

    .. versionchanged:: 2023.12
       Required that the output array must be one-dimensional.

    """

    @abstractmethod
    def __call__(self, x: TArray, /) -> TArray: ...


@runtime_checkable
class ArrayNamespace[TArray: Array, TDtype, TDevice](Protocol):
    astype: astype[TArray, TDtype, TDevice]
    "Copies an array to a specified data type irrespective of :ref:`type-promotion` rules.\n\n.. note::\n   Casting floating-point ``NaN`` and ``infinity`` values to integral data types is not specified and is implementation-dependent.\n\n.. note::\n   Casting a complex floating-point array to a real-valued data type should not be permitted.\n\n   Historically, when casting a complex floating-point array to a real-valued data type, libraries such as NumPy have discarded imaginary components such that, for a complex floating-point array ``x``, ``astype(x)`` equals ``astype(real(x))``). This behavior is considered problematic as the choice to discard the imaginary component is arbitrary and introduces more than one way to achieve the same outcome (i.e., for a complex floating-point array ``x``, ``astype(x)`` and ``astype(real(x))`` versus only ``astype(imag(x))``). Instead, in order to avoid ambiguity and to promote clarity, this specification requires that array API consumers explicitly express which component should be cast to a specified real-valued data type.\n\n.. note::\n   When casting a boolean input array to a real-valued data type, a value of ``True`` must cast to a real-valued number equal to ``1``, and a value of ``False`` must cast to a real-valued number equal to ``0``.\n\n   When casting a boolean input array to a complex floating-point data type, a value of ``True`` must cast to a complex number equal to ``1 + 0j``, and a value of ``False`` must cast to a complex number equal to ``0 + 0j``.\n\n.. note::\n   When casting a real-valued input array to ``bool``, a value of ``0`` must cast to ``False``, and a non-zero value must cast to ``True``.\n\n   When casting a complex floating-point array to ``bool``, a value of ``0 + 0j`` must cast to ``False``, and all other values must cast to ``True``.\n\nParameters\n----------\nx: array\n    array to cast.\ndtype: dtype\n    desired data type.\ncopy: bool\n    specifies whether to copy an array when the specified ``dtype`` matches the data type of the input array ``x``. If ``True``, a newly allocated array must always be returned. If ``False`` and the specified ``dtype`` matches the data type of the input array, the input array must be returned; otherwise, a newly allocated array must be returned. Default: ``True``.\ndevice: Optional[device]\n    device on which to place the returned array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array having the specified data type. The returned array must have the same shape as ``x``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Added device keyword argument support."
    can_cast: can_cast[TArray, TDtype]
    "Determines if one data type can be cast to another data type according :ref:`type-promotion` rules.\n\nParameters\n----------\nfrom_: Union[dtype, array]\n    input data type or array from which to cast.\nto: dtype\n    desired data type.\n\nReturns\n-------\nout: bool\n    ``True`` if the cast can occur according to :ref:`type-promotion` rules; otherwise, ``False``."
    finfo: finfo[TArray, TDtype]
    "Machine limits for floating-point data types.\n\nParameters\n----------\ntype: Union[dtype, array]\n    the kind of floating-point data-type about which to get information. If complex, the information is about its component data type.\n\n    .. note::\n       Complex floating-point data types are specified to always use the same precision for both its real and imaginary components, so the information should be true for either component.\n\nReturns\n-------\nout: finfo object\n    an object having the following attributes:\n\n    - **bits**: *int*\n\n      number of bits occupied by the real-valued floating-point data type.\n\n    - **eps**: *float*\n\n      difference between 1.0 and the next smallest representable real-valued floating-point number larger than 1.0 according to the IEEE-754 standard.\n\n    - **max**: *float*\n\n      largest representable real-valued number.\n\n    - **min**: *float*\n\n      smallest representable real-valued number.\n\n    - **smallest_normal**: *float*\n\n      smallest positive real-valued floating-point number with full precision.\n\n    - **dtype**: dtype\n\n      real-valued floating-point data type.\n\n      .. versionadded:: 2022.12\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    iinfo: iinfo[TArray, TDtype]
    "Machine limits for integer data types.\n\nParameters\n----------\ntype: Union[dtype, array]\n    the kind of integer data-type about which to get information.\n\nReturns\n-------\nout: iinfo object\n    an object having the following attributes:\n\n    - **bits**: *int*\n\n      number of bits occupied by the type.\n\n    - **max**: *int*\n\n      largest representable number.\n\n    - **min**: *int*\n\n      smallest representable number.\n\n    - **dtype**: dtype\n\n      integer data type.\n\n      .. versionadded:: 2022.12"
    isdtype: isdtype[TDtype,]
    "Returns a boolean indicating whether a provided dtype is of a specified data type \"kind\".\n\nParameters\n----------\ndtype: dtype\n    the input dtype.\nkind: Union[str, dtype, Tuple[Union[str, dtype], ...]]\n    data type kind.\n\n    -   If ``kind`` is a dtype, the function must return a boolean indicating whether the input ``dtype`` is equal to the dtype specified by ``kind``.\n    -   If ``kind`` is a string, the function must return a boolean indicating whether the input ``dtype`` is of a specified data type kind. The following dtype kinds must be supported:\n\n        -   ``'bool'``: boolean data types (e.g., ``bool``).\n        -   ``'signed integer'``: signed integer data types (e.g., ``int8``, ``int16``, ``int32``, ``int64``).\n        -   ``'unsigned integer'``: unsigned integer data types (e.g., ``uint8``, ``uint16``, ``uint32``, ``uint64``).\n        -   ``'integral'``: integer data types. Shorthand for ``('signed integer', 'unsigned integer')``.\n        -   ``'real floating'``: real-valued floating-point data types (e.g., ``float32``, ``float64``).\n        -   ``'complex floating'``: complex floating-point data types (e.g., ``complex64``, ``complex128``).\n        -   ``'numeric'``: numeric data types. Shorthand for ``('integral', 'real floating', 'complex floating')``.\n\n    -   If ``kind`` is a tuple, the tuple specifies a union of dtypes and/or kinds, and the function must return a boolean indicating whether the input ``dtype`` is either equal to a specified dtype or belongs to at least one specified data type kind.\n\n    .. note::\n       A conforming implementation of the array API standard is **not** limited to only including the dtypes described in this specification in the required data type kinds. For example, implementations supporting ``float16`` and ``bfloat16`` can include ``float16`` and ``bfloat16`` in the ``real floating`` data type kind. Similarly, implementations supporting ``int128`` can include ``int128`` in the ``signed integer`` data type kind.\n\n       In short, conforming implementations may extend data type kinds; however, data type kinds must remain consistent (e.g., only integer dtypes may belong to integer data type kinds and only floating-point dtypes may belong to floating-point data type kinds), and extensions must be clearly documented as such in library documentation.\n\nReturns\n-------\nout: bool\n    boolean indicating whether a provided dtype is of a specified data type kind.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    result_type: result_type[TArray, TDtype]
    "Returns the dtype that results from applying the type promotion rules (see :ref:`type-promotion`) to the arguments.\n\n.. note::\n   If provided mixed dtypes (e.g., integer and floating-point), the returned dtype will be implementation-specific.\n\nParameters\n----------\narrays_and_dtypes: Union[array, dtype]\n    an arbitrary number of input arrays and/or dtypes.\n\nReturns\n-------\nout: dtype\n    the dtype resulting from an operation involving the input arrays and dtypes."
    cumulative_sum: cumulative_sum[TArray, TDtype]
    "Calculates the cumulative sum of elements in the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\naxis: Optional[int]\n    axis along which a cumulative sum must be computed. If ``axis`` is negative, the function must determine the axis along which to compute a cumulative sum by counting from the last dimension.\n\n    If ``x`` is a one-dimensional array, providing an ``axis`` is optional; however, if ``x`` has more than one dimension, providing an ``axis`` is required.\n\ndtype: Optional[dtype]\n    data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:\n\n    -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.\n    -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).\n\n    If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.\n\ninclude_initial: bool\n    boolean indicating whether to include the initial value as the first value in the output. By convention, the initial value must be the additive identity (i.e., zero). Default: ``False``.\n\nReturns\n-------\nout: array\n    an array containing the cumulative sums. The returned array must have a data type as described by the ``dtype`` parameter above.\n\n    Let ``N`` be the size of the axis along which to compute the cumulative sum. The returned array must have a shape determined according to the following rules:\n\n    -   if ``include_initial`` is ``True``, the returned array must have the same shape as ``x``, except the size of the axis along which to compute the cumulative sum must be ``N+1``.\n    -   if ``include_initial`` is ``False``, the returned array must have the same shape as ``x``.\n\nNotes\n-----\n\n**Special Cases**\n\nFor both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.add`.\n\n.. versionadded:: 2023.12"
    max: max[TArray,]
    "Calculates the maximum value of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which maximum values must be computed. By default, the maximum value must be computed over the entire array. If a tuple of integers, maximum values must be computed over multiple axes. Default: ``None``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the maximum value was computed over the entire array, a zero-dimensional array containing the maximum value; otherwise, a non-zero-dimensional array containing the maximum values. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\nWhen the number of elements over which to compute the maximum value is zero, the maximum value is implementation-defined. Specification-compliant libraries may choose to raise an error, return a sentinel value (e.g., if ``x`` is a floating-point input array, return ``NaN``), or return the minimum possible value for the input array ``x`` data type (e.g., if ``x`` is a floating-point array, return ``-infinity``).\n\nThe order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a maximum value, specification-compliant libraries may choose to return either value.\n\nFor backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).\n\n**Special Cases**\n\nFor floating-point operands,\n\n-   If ``x_i`` is ``NaN``, the maximum value is ``NaN`` (i.e., ``NaN`` values propagate).\n\n.. versionchanged:: 2023.12\n   Clarified that the order of signed zeros is implementation-defined."
    mean: mean[TArray,]
    "Calculates the arithmetic mean of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued floating-point data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which arithmetic means must be computed. By default, the mean must be computed over the entire array. If a tuple of integers, arithmetic means must be computed over multiple axes. Default: ``None``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the arithmetic mean was computed over the entire array, a zero-dimensional array containing the arithmetic mean; otherwise, a non-zero-dimensional array containing the arithmetic means. The returned array must have the same data type as ``x``.\n\n    .. note::\n       While this specification recommends that this function only accept input arrays having a real-valued floating-point data type, specification-compliant array libraries may choose to accept input arrays having an integer data type. While mixed data type promotion is implementation-defined, if the input array ``x`` has an integer data type, the returned array must have the default real-valued floating-point data type.\n\nNotes\n-----\n\n**Special Cases**\n\nLet ``N`` equal the number of elements over which to compute the arithmetic mean.\n\n-   If ``N`` is ``0``, the arithmetic mean is ``NaN``.\n-   If ``x_i`` is ``NaN``, the arithmetic mean is ``NaN`` (i.e., ``NaN`` values propagate)."
    min: min[TArray,]
    "Calculates the minimum value of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which minimum values must be computed. By default, the minimum value must be computed over the entire array. If a tuple of integers, minimum values must be computed over multiple axes. Default: ``None``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the minimum value was computed over the entire array, a zero-dimensional array containing the minimum value; otherwise, a non-zero-dimensional array containing the minimum values. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\nWhen the number of elements over which to compute the minimum value is zero, the minimum value is implementation-defined. Specification-compliant libraries may choose to raise an error, return a sentinel value (e.g., if ``x`` is a floating-point input array, return ``NaN``), or return the maximum possible value for the input array ``x`` data type (e.g., if ``x`` is a floating-point array, return ``+infinity``).\n\nThe order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a minimum value, specification-compliant libraries may choose to return either value.\n\nFor backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).\n\n**Special Cases**\n\nFor floating-point operands,\n\n-   If ``x_i`` is ``NaN``, the minimum value is ``NaN`` (i.e., ``NaN`` values propagate).\n\n.. versionchanged:: 2023.12\n   Clarified that the order of signed zeros is implementation-defined."
    prod: prod[TArray, TDtype]
    "Calculates the product of input array ``x`` elements.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which products must be computed. By default, the product must be computed over the entire array. If a tuple of integers, products must be computed over multiple axes. Default: ``None``.\n\ndtype: Optional[dtype]\n    data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:\n\n    -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.\n    -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).\n\n    If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.\n\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the product was computed over the entire array, a zero-dimensional array containing the product; otherwise, a non-zero-dimensional array containing the products. The returned array must have a data type as described by the ``dtype`` parameter above.\n\nNotes\n-----\n\n**Special Cases**\n\nLet ``N`` equal the number of elements over which to compute the product.\n\n-   If ``N`` is ``0``, the product is `1` (i.e., the empty product).\n\nFor both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.multiply`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Required the function to return a floating-point array having the same data type as the input array when provided a floating-point array."
    std: std[TArray,]
    "Calculates the standard deviation of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued floating-point data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which standard deviations must be computed. By default, the standard deviation must be computed over the entire array. If a tuple of integers, standard deviations must be computed over multiple axes. Default: ``None``.\ncorrection: Union[int, float]\n    degrees of freedom adjustment. Setting this parameter to a value other than ``0`` has the effect of adjusting the divisor during the calculation of the standard deviation according to ``N-c`` where ``N`` corresponds to the total number of elements over which the standard deviation is computed and ``c`` corresponds to the provided degrees of freedom adjustment. When computing the standard deviation of a population, setting this parameter to ``0`` is the standard choice (i.e., the provided array contains data constituting an entire population). When computing the corrected sample standard deviation, setting this parameter to ``1`` is the standard choice (i.e., the provided array contains data sampled from a larger population; this is commonly referred to as Bessel's correction). Default: ``0``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the standard deviation was computed over the entire array, a zero-dimensional array containing the standard deviation; otherwise, a non-zero-dimensional array containing the standard deviations. The returned array must have the same data type as ``x``.\n\n    .. note::\n       While this specification recommends that this function only accept input arrays having a real-valued floating-point data type, specification-compliant array libraries may choose to accept input arrays having an integer data type. While mixed data type promotion is implementation-defined, if the input array ``x`` has an integer data type, the returned array must have the default real-valued floating-point data type.\n\nNotes\n-----\n\n**Special Cases**\n\nLet ``N`` equal the number of elements over which to compute the standard deviation.\n\n-   If ``N - correction`` is less than or equal to ``0``, the standard deviation is ``NaN``.\n-   If ``x_i`` is ``NaN``, the standard deviation is ``NaN`` (i.e., ``NaN`` values propagate)."
    sum: sum[TArray, TDtype]
    "Calculates the sum of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which sums must be computed. By default, the sum must be computed over the entire array. If a tuple of integers, sums must be computed over multiple axes. Default: ``None``.\n\ndtype: Optional[dtype]\n    data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:\n\n    -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.\n    -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).\n\n    If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.\n\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the sum was computed over the entire array, a zero-dimensional array containing the sum; otherwise, an array containing the sums. The returned array must have a data type as described by the ``dtype`` parameter above.\n\nNotes\n-----\n\n**Special Cases**\n\nLet ``N`` equal the number of elements over which to compute the sum.\n\n-   If ``N`` is ``0``, the sum is ``0`` (i.e., the empty sum).\n\nFor both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.add`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Required the function to return a floating-point array having the same data type as the input array when provided a floating-point array."
    var: var[TArray,]
    "Calculates the variance of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued floating-point data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which variances must be computed. By default, the variance must be computed over the entire array. If a tuple of integers, variances must be computed over multiple axes. Default: ``None``.\ncorrection: Union[int, float]\n    degrees of freedom adjustment. Setting this parameter to a value other than ``0`` has the effect of adjusting the divisor during the calculation of the variance according to ``N-c`` where ``N`` corresponds to the total number of elements over which the variance is computed and ``c`` corresponds to the provided degrees of freedom adjustment. When computing the variance of a population, setting this parameter to ``0`` is the standard choice (i.e., the provided array contains data constituting an entire population). When computing the unbiased sample variance, setting this parameter to ``1`` is the standard choice (i.e., the provided array contains data sampled from a larger population; this is commonly referred to as Bessel's correction). Default: ``0``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if the variance was computed over the entire array, a zero-dimensional array containing the variance; otherwise, a non-zero-dimensional array containing the variances. The returned array must have the same data type as ``x``.\n\n\n.. note::\n   While this specification recommends that this function only accept input arrays having a real-valued floating-point data type, specification-compliant array libraries may choose to accept input arrays having an integer data type. While mixed data type promotion is implementation-defined, if the input array ``x`` has an integer data type, the returned array must have the default real-valued floating-point data type.\n\nNotes\n-----\n\n**Special Cases**\n\nLet ``N`` equal the number of elements over which to compute the variance.\n\n-   If ``N - correction`` is less than or equal to ``0``, the variance is ``NaN``.\n-   If ``x_i`` is ``NaN``, the variance is ``NaN`` (i.e., ``NaN`` values propagate)."
    arange: arange[TArray, TDtype, TDevice]
    "Returns evenly spaced values within the half-open interval ``[start, stop)`` as a one-dimensional array.\n\nParameters\n----------\nstart: Union[int, float]\n    if ``stop`` is specified, the start of interval (inclusive); otherwise, the end of the interval (exclusive). If ``stop`` is not specified, the default starting value is ``0``.\nstop: Optional[Union[int, float]]\n    the end of the interval. Default: ``None``.\nstep: Union[int, float]\n    the distance between two adjacent elements (``out[i+1] - out[i]``). Must not be ``0``; may be negative, this results in an empty array if ``stop >= start``. Default: ``1``.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``start``, ``stop`` and ``step``. If those are all integers, the output array dtype must be the default integer dtype; if one or more have type ``float``, then the output array dtype must be the default real-valued floating-point data type. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\n\n.. note::\n   This function cannot guarantee that the interval does not include the ``stop`` value in those cases where ``step`` is not an integer and floating-point rounding errors affect the length of the output array.\n\nReturns\n-------\nout: array\n    a one-dimensional array containing evenly spaced values. The length of the output array must be ``ceil((stop-start)/step)`` if ``stop - start`` and ``step`` have the same sign, and length ``0`` otherwise."
    asarray: asarray[TArray, TDtype, TDevice]
    "Convert the input to an array.\n\nParameters\n----------\nobj: Union[array, bool, int, float, complex, NestedSequence[bool | int | float | complex], SupportsBufferProtocol]\n    object to be converted to an array. May be a Python scalar, a (possibly nested) sequence of Python scalars, or an object supporting the Python buffer protocol.\n\n    .. admonition:: Tip\n       :class: important\n\n       An object supporting the buffer protocol can be turned into a memoryview through ``memoryview(obj)``.\n\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from the data type(s) in ``obj``. If all input values are Python scalars, then, in order of precedence,\n\n    -   if all values are of type ``bool``, the output data type must be ``bool``.\n    -   if all values are of type ``int`` or are a mixture of ``bool`` and ``int``, the output data type must be the default integer data type.\n    -   if one or more values are ``complex`` numbers, the output data type must be the default complex floating-point data type.\n    -   if one or more values are ``float``\\s, the output data type must be the default real-valued floating-point data type.\n\n    Default: ``None``.\n\n    .. admonition:: Note\n       :class: note\n\n       If ``dtype`` is not ``None``, then array conversions should obey :ref:`type-promotion` rules. Conversions not specified according to :ref:`type-promotion` rules may or may not be permitted by a conforming array library. To perform an explicit cast, use :func:`array_api.astype`.\n\n    .. note::\n       If an input value exceeds the precision of the resolved output array data type, behavior is left unspecified and, thus, implementation-defined.\n\ndevice: Optional[device]\n    device on which to place the created array. If ``device`` is ``None`` and ``obj`` is an array, the output array device must be inferred from ``obj``. Default: ``None``.\ncopy: Optional[bool]\n    boolean indicating whether or not to copy the input. If ``True``, the function must always copy. If ``False``, the function must never copy for input which supports the buffer protocol and must raise a ``ValueError`` in case a copy would be necessary. If ``None``, the function must reuse existing memory buffer if possible and copy otherwise. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing the data from ``obj``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    empty: empty[TArray, TDtype, TDevice]
    "Returns an uninitialized array having a specified `shape`.\n\nParameters\n----------\nshape: Union[int, Tuple[int, ...]]\n    output array shape.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing uninitialized data."
    empty_like: empty_like[TArray, TDtype, TDevice]
    "Returns an uninitialized array with the same ``shape`` as an input array ``x``.\n\nParameters\n----------\nx: array\n    input array from which to derive the output array shape.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array having the same shape as ``x`` and containing uninitialized data."
    eye: eye[TArray, TDtype, TDevice]
    "Returns a two-dimensional array with ones on the ``k``\\th diagonal and zeros elsewhere.\n\n.. note::\n   An output array having a complex floating-point data type must have the value ``1 + 0j`` along the ``k``\\th diagonal and ``0 + 0j`` elsewhere.\n\nParameters\n----------\nn_rows: int\n    number of rows in the output array.\nn_cols: Optional[int]\n    number of columns in the output array. If ``None``, the default number of columns in the output array is equal to ``n_rows``. Default: ``None``.\nk: int\n    index of the diagonal. A positive value refers to an upper diagonal, a negative value to a lower diagonal, and ``0`` to the main diagonal. Default: ``0``.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array where all elements are equal to zero, except for the ``k``\\th diagonal, whose values are equal to one.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    from_dlpack: from_dlpack[TArray, TDevice]
    "Returns a new array containing the data from another (array) object with a ``__dlpack__`` method.\n\nParameters\n----------\nx: object\n    input (array) object.\ndevice: Optional[device]\n    device on which to place the created array. If ``device`` is ``None`` and ``x`` supports DLPack, the output array must be on the same device as ``x``. Default: ``None``.\n\n    The v2023.12 standard only mandates that a compliant library should offer a way for ``from_dlpack`` to return an array\n    whose underlying memory is accessible to the Python interpreter, when the corresponding ``device`` is provided. If the\n    array library does not support such cases at all, the function must raise ``BufferError``. If a copy must be made to\n    enable this support but ``copy`` is set to ``False``, the function must raise ``ValueError``.\n\n    Other device kinds will be considered for standardization in a future version of this API standard.\ncopy: Optional[bool]\n    boolean indicating whether or not to copy the input. If ``True``, the function must always copy. If ``False``, the function must never copy, and raise ``BufferError`` in case a copy is deemed necessary (e.g.  if a cross-device data movement is requested, and it is not possible without a copy). If ``None``, the function must reuse the existing memory buffer if possible and copy otherwise. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing the data in ``x``.\n\n    .. admonition:: Note\n       :class: note\n\n       The returned array may be either a copy or a view. See :ref:`data-interchange` for details.\n\nRaises\n------\nBufferError\n    The ``__dlpack__`` and ``__dlpack_device__`` methods on the input array\n    may raise ``BufferError`` when the data cannot be exported as DLPack\n    (e.g., incompatible dtype, strides, or device). It may also raise other errors\n    when export fails for other reasons (e.g., not enough memory available\n    to materialize the data). ``from_dlpack`` must propagate such\n    exceptions.\nAttributeError\n    If the ``__dlpack__`` and ``__dlpack_device__`` methods are not present\n    on the input array. This may happen for libraries that are never able\n    to export their data with DLPack.\nValueError\n    If data exchange is possible via an explicit copy but ``copy`` is set to ``False``.\n\nNotes\n-----\nSee :meth:`array.__dlpack__` for implementation suggestions for `from_dlpack` in\norder to handle DLPack versioning correctly.\n\nA way to move data from two array libraries to the same device (assumed supported by both libraries) in\na library-agnostic fashion is illustrated below:\n\n.. code:: python\n\n    def func(x, y):\n        xp_x = x.__array_namespace__()\n        xp_y = y.__array_namespace__()\n\n        # Other functions than `from_dlpack` only work if both arrays are from the same library. So if\n        # `y` is from a different one than `x`, let's convert `y` into an array of the same type as `x`:\n        if not xp_x == xp_y:\n            y = xp_x.from_dlpack(y, copy=True, device=x.device)\n\n        # From now on use `xp_x.xxxxx` functions, as both arrays are from the library `xp_x`\n        ...\n\n\n.. versionchanged:: 2023.12\n   Required exceptions to address unsupported use cases.\n\n.. versionchanged:: 2023.12\n   Added device and copy support."
    full: full[TArray, TDtype, TDevice]
    "Returns a new array having a specified ``shape`` and filled with ``fill_value``.\n\nParameters\n----------\nshape: Union[int, Tuple[int, ...]]\n    output array shape.\nfill_value: Union[bool, int, float, complex]\n    fill value.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``fill_value`` according to the following rules:\n\n    - If the fill value is an ``int``, the output array data type must be the default integer data type.\n    - If the fill value is a ``float``, the output array data type must be the default real-valued floating-point data type.\n    - If the fill value is a ``complex`` number, the output array data type must be the default complex floating-point data type.\n    - If the fill value is a ``bool``, the output array must have a boolean data type. Default: ``None``.\n\n    .. note::\n       If the ``fill_value`` exceeds the precision of the resolved default output array data type, behavior is left unspecified and, thus, implementation-defined.\n\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array where every element is equal to ``fill_value``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    full_like: full_like[TArray, TDtype, TDevice]
    "Returns a new array filled with ``fill_value`` and having the same ``shape`` as an input array ``x``.\n\nParameters\n----------\nx: array\n    input array from which to derive the output array shape.\nfill_value: Union[bool, int, float, complex]\n    fill value.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.\n\n    .. note::\n       If the ``fill_value`` exceeds the precision of the resolved output array data type, behavior is unspecified and, thus, implementation-defined.\n\n    .. note::\n       If the ``fill_value`` has a data type which is not of the same data type kind (boolean, integer, or floating-point) as the resolved output array data type (see :ref:`type-promotion`), behavior is unspecified and, thus, implementation-defined.\n\ndevice: Optional[device]\n    device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array having the same shape as ``x`` and where every element is equal to ``fill_value``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    linspace: linspace[TArray, TDtype, TDevice]
    "Returns evenly spaced numbers over a specified interval.\n\nLet :math:`N` be the number of generated values (which is either ``num`` or ``num+1`` depending on whether ``endpoint`` is ``True`` or ``False``, respectively). For real-valued output arrays, the spacing between values is given by\n\n.. math::\n   \\Delta_{\\textrm{real}} = \\frac{\\textrm{stop} - \\textrm{start}}{N - 1}\n\nFor complex output arrays, let ``a = real(start)``, ``b = imag(start)``, ``c = real(stop)``, and ``d = imag(stop)``. The spacing between complex values is given by\n\n.. math::\n   \\Delta_{\\textrm{complex}} = \\frac{c-a}{N-1} + \\frac{d-b}{N-1} j\n\nParameters\n----------\nstart: Union[int, float, complex]\n    the start of the interval.\nstop: Union[int, float, complex]\n    the end of the interval. If ``endpoint`` is ``False``, the function must generate a sequence of ``num+1`` evenly spaced numbers starting with ``start`` and ending with ``stop`` and exclude the ``stop`` from the returned array such that the returned array consists of evenly spaced numbers over the half-open interval ``[start, stop)``. If ``endpoint`` is ``True``, the output array must consist of evenly spaced numbers over the closed interval ``[start, stop]``. Default: ``True``.\n\n    .. note::\n       The step size changes when `endpoint` is `False`.\n\nnum: int\n    number of samples. Must be a nonnegative integer value.\ndtype: Optional[dtype]\n    output array data type. Should be a floating-point data type. If ``dtype`` is ``None``,\n\n    -   if either ``start`` or ``stop`` is a ``complex`` number, the output data type must be the default complex floating-point data type.\n    -   if both ``start`` and ``stop`` are real-valued, the output data type must be the default real-valued floating-point data type.\n\n    Default: ``None``.\n\n    .. admonition:: Note\n       :class: note\n\n       If ``dtype`` is not ``None``, conversion of ``start`` and ``stop`` should obey :ref:`type-promotion` rules. Conversions not specified according to :ref:`type-promotion` rules may or may not be permitted by a conforming array library.\n\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\nendpoint: bool\n    boolean indicating whether to include ``stop`` in the interval. Default: ``True``.\n\nReturns\n-------\nout: array\n    a one-dimensional array containing evenly spaced values.\n\nNotes\n-----\n\n.. note::\n   While this specification recommends that this function only return arrays having a floating-point data type, specification-compliant array libraries may choose to support output arrays having an integer data type (e.g., due to backward compatibility concerns). However, function behavior when generating integer output arrays is unspecified and, thus, is implementation-defined. Accordingly, using this function to generate integer output arrays is not portable.\n\n.. note::\n   As mixed data type promotion is implementation-defined, behavior when ``start`` or ``stop`` exceeds the maximum safe integer of an output floating-point data type is implementation-defined. An implementation may choose to overflow or raise an exception.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    meshgrid: meshgrid[TArray,]
    "Returns coordinate matrices from coordinate vectors.\n\nParameters\n----------\narrays: array\n    an arbitrary number of one-dimensional arrays representing grid coordinates. Each array should have the same numeric data type.\nindexing:  Literal[\"xy\", \"ij\"]\n    Cartesian ``'xy'`` or matrix ``'ij'`` indexing of output. If provided zero or one one-dimensional vector(s) (i.e., the zero- and one-dimensional cases, respectively), the ``indexing`` keyword has no effect and should be ignored. Default: ``'xy'``.\n\nReturns\n-------\nout: List[array]\n    list of N arrays, where ``N`` is the number of provided one-dimensional input arrays. Each returned array must have rank ``N``. For ``N`` one-dimensional arrays having lengths ``Ni = len(xi)``,\n\n    - if matrix indexing ``ij``, then each returned array must have the shape ``(N1, N2, N3, ..., Nn)``.\n    - if Cartesian indexing ``xy``, then each returned array must have shape ``(N2, N1, N3, ..., Nn)``.\n\n    Accordingly, for the two-dimensional case with input one-dimensional arrays of length ``M`` and ``N``, if matrix indexing ``ij``, then each returned array must have shape ``(M, N)``, and, if Cartesian indexing ``xy``, then each returned array must have shape ``(N, M)``.\n\n    Similarly, for the three-dimensional case with input one-dimensional arrays of length ``M``, ``N``, and ``P``, if matrix indexing ``ij``, then each returned array must have shape ``(M, N, P)``, and, if Cartesian indexing ``xy``, then each returned array must have shape ``(N, M, P)``.\n\n    Each returned array should have the same data type as the input arrays.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    ones: ones[TArray, TDtype, TDevice]
    "Returns a new array having a specified ``shape`` and filled with ones.\n\n.. note::\n   An output array having a complex floating-point data type must contain complex numbers having a real component equal to one and an imaginary component equal to zero (i.e., ``1 + 0j``).\n\nParameters\n----------\nshape: Union[int, Tuple[int, ...]]\n    output array shape.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing ones.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    ones_like: ones_like[TArray, TDtype, TDevice]
    "Returns a new array filled with ones and having the same ``shape`` as an input array ``x``.\n\n.. note::\n   An output array having a complex floating-point data type must contain complex numbers having a real component equal to one and an imaginary component equal to zero (i.e., ``1 + 0j``).\n\nParameters\n----------\nx: array\n    input array from which to derive the output array shape.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array having the same shape as ``x`` and filled with ones.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    tril: tril[TArray,]
    "Returns the lower triangular part of a matrix (or a stack of matrices) ``x``.\n\n.. note::\n   The lower triangular part of the matrix is defined as the elements on and below the specified diagonal ``k``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.\nk: int\n    diagonal above which to zero elements. If ``k = 0``, the diagonal is the main diagonal. If ``k < 0``, the diagonal is below the main diagonal. If ``k > 0``, the diagonal is above the main diagonal. Default: ``0``.\n\n    .. note::\n       The main diagonal is defined as the set of indices ``{(i, i)}`` for ``i`` on the interval ``[0, min(M, N) - 1]``.\n\nReturns\n-------\nout: array\n    an array containing the lower triangular part(s). The returned array must have the same shape and data type as ``x``. All elements above the specified diagonal ``k`` must be zeroed. The returned array should be allocated on the same device as ``x``."
    triu: triu[TArray,]
    "Returns the upper triangular part of a matrix (or a stack of matrices) ``x``.\n\n.. note::\n   The upper triangular part of the matrix is defined as the elements on and above the specified diagonal ``k``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.\nk: int\n    diagonal below which to zero elements. If ``k = 0``, the diagonal is the main diagonal. If ``k < 0``, the diagonal is below the main diagonal. If ``k > 0``, the diagonal is above the main diagonal. Default: ``0``.\n\n    .. note::\n       The main diagonal is defined as the set of indices ``{(i, i)}`` for ``i`` on the interval ``[0, min(M, N) - 1]``.\n\nReturns\n-------\nout: array\n    an array containing the upper triangular part(s). The returned array must have the same shape and data type as ``x``. All elements below the specified diagonal ``k`` must be zeroed. The returned array should be allocated on the same device as ``x``."
    zeros: zeros[TArray, TDtype, TDevice]
    "Returns a new array having a specified ``shape`` and filled with zeros.\n\nParameters\n----------\nshape: Union[int, Tuple[int, ...]]\n    output array shape.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be the default real-valued floating-point data type. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing zeros."
    zeros_like: zeros_like[TArray, TDtype, TDevice]
    "Returns a new array filled with zeros and having the same ``shape`` as an input array ``x``.\n\nParameters\n----------\nx: array\n    input array from which to derive the output array shape.\ndtype: Optional[dtype]\n    output array data type. If ``dtype`` is ``None``, the output array data type must be inferred from ``x``. Default: ``None``.\ndevice: Optional[device]\n    device on which to place the created array. If ``device`` is ``None``, the output array device must be inferred from ``x``. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array having the same shape as ``x`` and filled with zeros."
    argsort: argsort[TArray,]
    "Returns the indices that sort an array ``x`` along a specified axis.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx : array\n    input array. Should have a real-valued data type.\naxis: int\n    axis along which to sort. If set to ``-1``, the function must sort along the last axis. Default: ``-1``.\ndescending: bool\n    sort order. If ``True``, the returned indices sort ``x`` in descending order (by value). If ``False``, the returned indices sort ``x`` in ascending order (by value). Default: ``False``.\nstable: bool\n    sort stability. If ``True``, the returned indices must maintain the relative order of ``x`` values which compare as equal. If ``False``, the returned indices may or may not maintain the relative order of ``x`` values which compare as equal (i.e., the relative order of ``x`` values which compare as equal is implementation-dependent). Default: ``True``.\n\nReturns\n-------\nout : array\n    an array of indices. The returned array must have the same shape as ``x``. The returned array must have the default array index data type."
    sort: sort[TArray,]
    "Returns a sorted copy of an input array ``x``.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\naxis: int\n    axis along which to sort. If set to ``-1``, the function must sort along the last axis. Default: ``-1``.\ndescending: bool\n    sort order. If ``True``, the array must be sorted in descending order (by value). If ``False``, the array must be sorted in ascending order (by value). Default: ``False``.\nstable: bool\n    sort stability. If ``True``, the returned array must maintain the relative order of ``x`` values which compare as equal. If ``False``, the returned array may or may not maintain the relative order of ``x`` values which compare as equal (i.e., the relative order of ``x`` values which compare as equal is implementation-dependent). Default: ``True``.\n\nReturns\n-------\nout : array\n    a sorted array. The returned array must have the same data type and shape as ``x``."
    abs: abs[TArray,]
    "Calculates the absolute value for each element ``x_i`` of the input array ``x``.\n\nFor real-valued input arrays, the element-wise result has the same magnitude as the respective element in ``x`` but has positive sign.\n\n.. note::\n   For signed integer data types, the absolute value of the minimum representable integer is implementation-dependent.\n\n.. note::\n   For complex floating-point operands, the complex absolute value is known as the norm, modulus, or magnitude and, for a complex number :math:`z = a + bj` is computed as\n\n   .. math::\n      \\operatorname{abs}(z) = \\sqrt{a^2 + b^2}\n\n.. note::\n   For complex floating-point operands, conforming implementations should take care to avoid undue overflow or underflow during intermediate stages of computation.\n\n..\n   TODO: once ``hypot`` is added to the specification, remove the special cases for complex floating-point operands and the note concerning guarding against undue overflow/underflow, and state that special cases must be handled as if implemented as ``hypot(real(x), imag(x))``.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the absolute value of each element in ``x``. If ``x`` has a real-valued data type, the returned array must have the same data type as ``x``. If ``x`` has a complex floating-point data type, the returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type).\n\nNotes\n-----\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``-0``, the result is ``+0``.\n- If ``x_i`` is ``-infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is any value (including ``NaN``), the result is ``+infinity``.\n- If ``a`` is any value (including ``NaN``) and ``b`` is either ``+infinity`` or ``-infinity``, the result is ``+infinity``.\n- If ``a`` is either ``+0`` or ``-0``, the result is equal to ``abs(b)``.\n- If ``b`` is either ``+0`` or ``-0``, the result is equal to ``abs(a)``.\n- If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    acos: acos[TArray,]
    "Calculates an implementation-dependent approximation of the principal value of the inverse cosine for each element ``x_i`` of the input array ``x``.\n\nEach element-wise result is expressed in radians.\n\n.. note::\n   The principal value of the arc cosine of a complex number :math:`z` is\n\n   .. math::\n      \\operatorname{acos}(z) = \\frac{1}{2}\\pi + j\\ \\ln(zj + \\sqrt{1-z^2})\n\n   For any :math:`z`,\n\n   .. math::\n      \\operatorname{acos}(z) = \\pi - \\operatorname{acos}(-z)\n\n.. note::\n   For complex floating-point operands, ``acos(conj(x))`` must equal ``conj(acos(x))``.\n\n.. note::\n   The inverse cosine (or arc cosine) is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty, -1)` and :math:`(1, \\infty)` of the real axis.\n\n   Accordingly, for complex arguments, the function returns the inverse cosine in the range of a strip unbounded along the imaginary axis and in the interval :math:`[0, \\pi]` along the real axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is greater than ``1``, the result is ``NaN``.\n- If ``x_i`` is less than ``-1``, the result is ``NaN``.\n- If ``x_i`` is ``1``, the result is ``+0``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``π/2 - 0j``.\n- If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``NaN``, the result is ``π/2 + NaN j``.\n- If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``π/2 - infinity j``.\n- If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``π - infinity j``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+0 - infinity j``.\n- If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``3π/4 - infinity j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``π/4 - infinity j``.\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``NaN ± infinity j`` (sign of the imaginary component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``NaN - infinity j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    acosh: acosh[TArray,]
    "Calculates an implementation-dependent approximation to the inverse hyperbolic cosine for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   The principal value of the inverse hyperbolic cosine of a complex number :math:`z` is\n\n   .. math::\n      \\operatorname{acosh}(z) = \\ln(z + \\sqrt{z+1}\\sqrt{z-1})\n\n   For any :math:`z`,\n\n   .. math::\n      \\operatorname{acosh}(z) = \\frac{\\sqrt{z-1}}{\\sqrt{1-z}}\\operatorname{acos}(z)\n\n   or simply\n\n   .. math::\n      \\operatorname{acosh}(z) = j\\ \\operatorname{acos}(z)\n\n   in the upper half of the complex plane.\n\n.. note::\n   For complex floating-point operands, ``acosh(conj(x))`` must equal ``conj(acosh(x))``.\n\n.. note::\n   The inverse hyperbolic cosine is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segment :math:`(-\\infty, 1)` of the real axis.\n\n   Accordingly, for complex arguments, the function returns the inverse hyperbolic cosine in the interval :math:`[0, \\infty)` along the real axis and in the interval :math:`[-\\pi j, +\\pi j]` along the imaginary axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array whose elements each represent the area of a hyperbolic sector. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse hyperbolic cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``1``, the result is ``NaN``.\n- If ``x_i`` is ``1``, the result is ``+0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``+0 + πj/2``.\n- If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.\n- If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``NaN ± πj/2`` (sign of imaginary component is unspecified).\n- If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + πj``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.\n- If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + 3πj/4``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    add: add[TArray,]
    "Calculates the sum for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. Should have a numeric data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise sums. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``-infinity``, the result is ``NaN``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``+infinity``, the result is ``NaN``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``-infinity``, the result is ``-infinity``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a finite number, the result is ``+infinity``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a finite number, the result is ``-infinity``.\n- If ``x1_i`` is a finite number and ``x2_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x1_i`` is a finite number and ``x2_i`` is ``-infinity``, the result is ``-infinity``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is ``-0``, the result is ``-0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is ``+0``, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is ``-0``, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is ``+0``, the result is ``+0``.\n- If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is a nonzero finite number, the result is ``x2_i``.\n- If ``x1_i`` is a nonzero finite number and ``x2_i`` is either ``+0`` or ``-0``, the result is ``x1_i``.\n- If ``x1_i`` is a nonzero finite number and ``x2_i`` is ``-x1_i``, the result is ``+0``.\n- In the remaining cases, when neither ``infinity``, ``+0``, ``-0``, nor a ``NaN`` is involved, and the operands have the same mathematical sign or have different magnitudes, the sum must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported round mode. If the magnitude is too large to represent, the operation overflows and the result is an `infinity` of appropriate mathematical sign.\n\n.. note::\n   Floating-point addition is a commutative operation, but not always associative.\n\nFor complex floating-point operands, addition is defined according to the following table. For real components ``a`` and ``c`` and imaginary components ``b`` and ``d``,\n\n+------------+------------+------------+----------------+\n|            | c          | dj         | c + dj         |\n+============+============+============+================+\n| **a**      | a + c      | a + dj     | (a+c) + dj     |\n+------------+------------+------------+----------------+\n| **bj**     | c + bj     | (b+d)j     | c + (b+d)j     |\n+------------+------------+------------+----------------+\n| **a + bj** | (a+c) + bj | a + (b+d)j | (a+c) + (b+d)j |\n+------------+------------+------------+----------------+\n\nFor complex floating-point operands, real-valued floating-point special cases must independently apply to the real and imaginary component operations involving real numbers as described in the above table. For example, let ``a = real(x1_i)``, ``b = imag(x1_i)``, ``c = real(x2_i)``, ``d = imag(x2_i)``, and\n\n- If ``a`` is ``-0`` and ``c`` is ``-0``, the real component of the result is ``-0``.\n- Similarly, if ``b`` is ``+0`` and ``d`` is ``-0``, the imaginary component of the result is ``+0``.\n\nHence, if ``z1 = a + bj = -0 + 0j`` and ``z2 = c + dj = -0 - 0j``, the result of ``z1 + z2`` is ``-0 + 0j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    asin: asin[TArray,]
    "Calculates an implementation-dependent approximation of the principal value of the inverse sine for each element ``x_i`` of the input array ``x``.\n\nEach element-wise result is expressed in radians.\n\n.. note::\n   The principal value of the arc sine of a complex number :math:`z` is\n\n   .. math::\n      \\operatorname{asin}(z) = -j\\ \\ln(zj + \\sqrt{1-z^2})\n\n   For any :math:`z`,\n\n   .. math::\n      \\operatorname{asin}(z) = \\operatorname{acos}(-z) - \\frac{\\pi}{2}\n\n.. note::\n   For complex floating-point operands, ``asin(conj(x))`` must equal ``conj(asin(x))``.\n\n.. note::\n   The inverse sine (or arc sine) is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty, -1)` and :math:`(1, \\infty)` of the real axis.\n\n   Accordingly, for complex arguments, the function returns the inverse sine in the range of a strip unbounded along the imaginary axis and in the interval :math:`[-\\pi/2, +\\pi/2]` along the real axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is greater than ``1``, the result is ``NaN``.\n- If ``x_i`` is less than ``-1``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * asinh(x*1j)``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    asinh: asinh[TArray,]
    "Calculates an implementation-dependent approximation to the inverse hyperbolic sine for each element ``x_i`` in the input array ``x``.\n\n.. note::\n   The principal value of the inverse hyperbolic sine of a complex number :math:`z` is\n\n   .. math::\n      \\operatorname{asinh}(z) = \\ln(z + \\sqrt{1+z^2})\n\n   For any :math:`z`,\n\n   .. math::\n      \\operatorname{asinh}(z) = \\frac{\\operatorname{asin}(zj)}{j}\n\n.. note::\n   For complex floating-point operands, ``asinh(conj(x))`` must equal ``conj(asinh(x))`` and ``asinh(-z)`` must equal ``-asinh(z)``.\n\n.. note::\n   The inverse hyperbolic sine is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty j, -j)` and :math:`(j, \\infty j)` of the imaginary axis.\n\n   Accordingly, for complex arguments, the function returns the inverse hyperbolic sine in the range of a strip unbounded along the real axis and in the interval :math:`[-\\pi j/2, +\\pi j/2]` along the imaginary axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array whose elements each represent the area of a hyperbolic sector. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse hyperbolic sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.\n- If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.\n- If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.\n- If ``a`` is ``NaN`` and ``b`` is a nonzero finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``±infinity + NaN j`` (sign of the real component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    atan: atan[TArray,]
    "Calculates an implementation-dependent approximation of the principal value of the inverse tangent for each element ``x_i`` of the input array ``x``.\n\nEach element-wise result is expressed in radians.\n\n.. note::\n   The principal value of the inverse tangent of a complex number :math:`z` is\n\n   .. math::\n      \\operatorname{atan}(z) = -\\frac{\\ln(1 - zj) - \\ln(1 + zj)}{2}j\n\n.. note::\n   For complex floating-point operands, ``atan(conj(x))`` must equal ``conj(atan(x))``.\n\n.. note::\n   The inverse tangent (or arc tangent) is a multi-valued function and requires a branch on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty j, -j)` and :math:`(+j, \\infty j)` of the imaginary axis.\n\n   Accordingly, for complex arguments, the function returns the inverse tangent in the range of a strip unbounded along the imaginary axis and in the interval :math:`[-\\pi/2, +\\pi/2]` along the real axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+infinity``, the result is an implementation-dependent approximation to ``+π/2``.\n- If ``x_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``-π/2``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * atanh(x*1j)``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    atan2: atan2[TArray,]
    'Calculates an implementation-dependent approximation of the inverse tangent of the quotient ``x1/x2``, having domain ``[-infinity, +infinity] x [-infinity, +infinity]`` (where the ``x`` notation denotes the set of ordered pairs of elements ``(x1_i, x2_i)``) and codomain ``[-π, +π]``, for each pair of elements ``(x1_i, x2_i)`` of the input arrays ``x1`` and ``x2``, respectively. Each element-wise result is expressed in radians.\n\nThe mathematical signs of ``x1_i`` and ``x2_i`` determine the quadrant of each element-wise result. The quadrant (i.e., branch) is chosen such that each element-wise result is the signed angle in radians between the ray ending at the origin and passing through the point ``(1,0)`` and the ray ending at the origin and passing through the point ``(x2_i, x1_i)``.\n\n.. note::\n   Note the role reversal: the "y-coordinate" is the first function parameter; the "x-coordinate" is the second function parameter. The parameter order is intentional and traditional for the two-argument inverse tangent function where the y-coordinate argument is first and the x-coordinate argument is second.\n\nBy IEEE 754 convention, the inverse tangent of the quotient ``x1/x2`` is defined for ``x2_i`` equal to positive or negative zero and for either or both of ``x1_i`` and ``x2_i`` equal to positive or negative ``infinity``.\n\nParameters\n----------\nx1: array\n    input array corresponding to the y-coordinates. Should have a real-valued floating-point data type.\nx2: array\n    input array corresponding to the x-coordinates. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse tangent of the quotient ``x1/x2``. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is an implementation-dependent approximation to ``+π/2``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``+π/2``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is ``+0``, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``+π``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is an implementation-dependent approximation to ``+π``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``-0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is ``+0``, the result is ``-0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``-π``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is an implementation-dependent approximation to ``-π``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is an implementation-dependent approximation to ``-π/2``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is an implementation-dependent approximation to ``-π/2``.\n- If ``x1_i`` is greater than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``+infinity``, the result is ``+0``.\n- If ``x1_i`` is greater than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``+π``.\n- If ``x1_i`` is less than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``+infinity``, the result is ``-0``.\n- If ``x1_i`` is less than ``0``, ``x1_i`` is a finite number, and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``-π``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a finite number, the result is an implementation-dependent approximation to ``+π/2``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a finite number, the result is an implementation-dependent approximation to ``-π/2``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``+infinity``, the result is an implementation-dependent approximation to ``+π/4``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``+3π/4``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``+infinity``, the result is an implementation-dependent approximation to ``-π/4``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``-infinity``, the result is an implementation-dependent approximation to ``-3π/4``.'
    atanh: atanh[TArray,]
    "Calculates an implementation-dependent approximation to the inverse hyperbolic tangent for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   The principal value of the inverse hyperbolic tangent of a complex number :math:`z` is\n\n   .. math::\n      \\operatorname{atanh}(z) = \\frac{\\ln(1+z)-\\ln(z-1)}{2}\n\n   For any :math:`z`,\n\n   .. math::\n      \\operatorname{atanh}(z) = \\frac{\\operatorname{atan}(zj)}{j}\n\n.. note::\n   For complex floating-point operands, ``atanh(conj(x))`` must equal ``conj(atanh(x))`` and ``atanh(-x)`` must equal ``-atanh(x)``.\n\n.. note::\n   The inverse hyperbolic tangent is a multi-valued function and requires a branch cut on the complex plane. By convention, a branch cut is placed at the line segments :math:`(-\\infty, 1]` and :math:`[1, \\infty)` of the real axis.\n\n   Accordingly, for complex arguments, the function returns the inverse hyperbolic tangent in the range of a half-strip unbounded along the real axis and in the interval :math:`[-\\pi j/2, +\\pi j/2]` along the imaginary axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array whose elements each represent the area of a hyperbolic sector. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the inverse hyperbolic tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``-1``, the result is ``NaN``.\n- If ``x_i`` is greater than ``1``, the result is ``NaN``.\n- If ``x_i`` is ``-1``, the result is ``-infinity``.\n- If ``x_i`` is ``+1``, the result is ``+infinity``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.\n- If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``+0 + NaN j``.\n- If ``a`` is ``1`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.\n- If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``+infinity``, the result is ``+0 + πj/2``.\n- If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+0 + πj/2``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+0 + πj/2``.\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``+0 + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``±0 + πj/2`` (sign of the real component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    bitwise_and: bitwise_and[TArray,]
    "Computes the bitwise AND of the underlying binary representation of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. Should have an integer or boolean data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer or boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`."
    bitwise_left_shift: bitwise_left_shift[TArray,]
    "Shifts the bits of each element ``x1_i`` of the input array ``x1`` to the left by appending ``x2_i`` (i.e., the respective element in the input array ``x2``) zeros to the right of ``x1_i``.\n\nParameters\n----------\nx1: array\n    first input array. Should have an integer data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer data type. Each element must be greater than or equal to ``0``.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`."
    bitwise_invert: bitwise_invert[TArray,]
    "Inverts (flips) each bit for each element ``x_i`` of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have an integer or boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have the same data type as ``x``."
    bitwise_or: bitwise_or[TArray,]
    "Computes the bitwise OR of the underlying binary representation of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. Should have an integer or boolean data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer or boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`."
    bitwise_right_shift: bitwise_right_shift[TArray,]
    "Shifts the bits of each element ``x1_i`` of the input array ``x1`` to the right according to the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   This operation must be an arithmetic shift (i.e., sign-propagating) and thus equivalent to floor division by a power of two.\n\nParameters\n----------\nx1: array\n    first input array. Should have an integer data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer data type. Each element must be greater than or equal to ``0``.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`."
    bitwise_xor: bitwise_xor[TArray,]
    "Computes the bitwise XOR of the underlying binary representation of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. Should have an integer or boolean data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have an integer or boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`."
    ceil: ceil[TArray,]
    "Rounds each element ``x_i`` of the input array ``x`` to the smallest (i.e., closest to ``-infinity``) integer-valued number that is not less than ``x_i``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n**Special cases**\n\n- If ``x_i`` is already integer-valued, the result is ``x_i``.\n\nFor floating-point operands,\n\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-infinity``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``NaN``, the result is ``NaN``."
    clip: clip[TArray,]
    "Clamps each element ``x_i`` of the input array ``x`` to the range ``[min, max]``.\n\nParameters\n----------\nx: array\n  input array. Should have a real-valued data type.\nmin: Optional[Union[int, float, array]]\n  lower-bound of the range to which to clamp. If ``None``, no lower bound must be applied. Must be compatible with ``x`` and ``max`` (see :ref:`broadcasting`). Should have a real-valued data type. Default: ``None``.\nmax: Optional[Union[int, float, array]]\n  upper-bound of the range to which to clamp. If ``None``, no upper bound must be applied. Must be compatible with ``x`` and ``min`` (see :ref:`broadcasting`). Should have a real-valued data type. Default: ``None``.\n\nReturns\n-------\nout: array\n  an array containing element-wise results. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n- If both ``min`` and ``max`` are ``None``, the elements of the returned array must equal the respective elements in ``x``.\n- If a broadcasted element in ``min`` is greater than a corresponding broadcasted element in ``max``, behavior is unspecified and thus implementation-dependent.\n- If ``x`` has an integral data type and a broadcasted element in ``min`` or ``max`` is outside the bounds of the data type of ``x``, behavior is unspecified and thus implementation-dependent.\n- If ``x`` and either ``min`` or ``max`` have different data type kinds (e.g., integer versus floating-point), behavior is unspecified and thus implementation-dependent.\n- For scalar ``min`` and/or ``max``, the scalar values should follow type promotion rules for operations involving arrays and scalar operands (see :ref:`type-promotion`).\n\n**Special cases**\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``min_i`` is ``NaN``, the result is ``NaN``.\n- If ``max_i`` is ``NaN``, the result is ``NaN``.\n\n.. versionadded:: 2023.12"
    conj: conj[TArray,]
    "Returns the complex conjugate for each element ``x_i`` of the input array ``x``.\n\nFor complex numbers of the form\n\n.. math::\n   a + bj\n\nthe complex conjugate is defined as\n\n.. math::\n   a - bj\n\nHence, the returned complex conjugates must be computed by negating the imaginary component of each element ``x_i``.\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    copysign: copysign[TArray,]
    "Composes a floating-point value with the magnitude of ``x1_i`` and the sign of ``x2_i`` for each element of the input array ``x1``.\n\nParameters\n----------\nx1: array\n   input array containing magnitudes. Should have a real-valued floating-point data type.\nx2: array\n   input array whose sign bits are applied to the magnitudes of ``x1``. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.\n\nReturns\n-------\nout: array\n   an array containing the element-wise results. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands, let ``|x|`` be the absolute value, and if ``x1_i`` is not ``NaN``,\n\n- If ``x2_i`` is less than ``0``, the result is ``-|x1_i|``.\n- If ``x2_i`` is ``-0``, the result is ``-|x1_i|``.\n- If ``x2_i`` is ``+0``, the result is ``|x1_i|``.\n- If ``x2_i`` is greater than ``0``, the result is ``|x1_i|``.\n- If ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``1``, the result is ``-|x1_i|``.\n- If ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``0``, the result is ``|x1_i|``.\n\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is less than ``0``, the result is ``NaN`` with a sign bit of ``1``.\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is ``-0``, the result is ``NaN`` with a sign bit of ``1``.\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is ``+0``, the result is ``NaN`` with a sign bit of ``0``.\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is greater than ``0``, the result is ``NaN`` with a sign bit of ``0``.\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``1``, the result is ``NaN`` with a sign bit of ``1``.\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is ``NaN`` and the sign bit of ``x2_i`` is ``0``, the result is ``NaN`` with a sign bit of ``0``.\n\n.. versionadded:: 2023.12"
    cos: cos[TArray,]
    "Calculates an implementation-dependent approximation to the cosine for each element ``x_i`` of the input array ``x``.\n\nEach element ``x_i`` is assumed to be expressed in radians.\n\n.. note::\n   The cosine is an entire function on the complex plane and has no branch cuts.\n\n.. note::\n   For complex arguments, the mathematical definition of cosine is\n\n   .. math::\n      \\begin{align} \\operatorname{cos}(x) &= \\sum_{n=0}^\\infty \\frac{(-1)^n}{(2n)!} x^{2n} \\\\ &= \\frac{e^{jx} + e^{-jx}}{2} \\\\ &= \\operatorname{cosh}(jx) \\end{align}\n\n   where :math:`\\operatorname{cosh}` is the hyperbolic cosine.\n\nParameters\n----------\nx: array\n    input array whose elements are each expressed in radians. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``1``.\n- If ``x_i`` is ``-0``, the result is ``1``.\n- If ``x_i`` is ``+infinity``, the result is ``NaN``.\n- If ``x_i`` is ``-infinity``, the result is ``NaN``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented as ``cosh(x*1j)``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    cosh: cosh[TArray,]
    "Calculates an implementation-dependent approximation to the hyperbolic cosine for each element ``x_i`` in the input array ``x``.\n\nThe mathematical definition of the hyperbolic cosine is\n\n.. math::\n   \\operatorname{cosh}(x) = \\frac{e^x + e^{-x}}{2}\n\n.. note::\n   The hyperbolic cosine is an entire function in the complex plane and has no branch cuts. The function is periodic, with period :math:`2\\pi j`, with respect to the imaginary component.\n\nParameters\n----------\nx: array\n    input array whose elements each represent a hyperbolic angle. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the hyperbolic cosine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\n.. note::\n   For all operands, ``cosh(x)`` must equal ``cosh(-x)``.\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``1``.\n- If ``x_i`` is ``-0``, the result is ``1``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n.. note::\n   For complex floating-point operands, ``cosh(conj(x))`` must equal ``conj(cosh(x))``.\n\n- If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``1 + 0j``.\n- If ``a`` is ``+0`` and ``b`` is ``+infinity``, the result is ``NaN + 0j`` (sign of the imaginary component is unspecified).\n- If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``NaN + 0j`` (sign of the imaginary component is unspecified).\n- If ``a`` is a nonzero finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.\n- If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.\n- If ``a`` is ``+infinity`` and ``b`` is a nonzero finite number, the result is ``+infinity * cis(b)``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j`` (sign of the real component is unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is either ``+0`` or ``-0``, the result is ``NaN + 0j`` (sign of the imaginary component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is a nonzero finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\nwhere ``cis(v)`` is ``cos(v) + sin(v)*1j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    divide: divide[TArray,]
    'Calculates the division of each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   If one or both of the input arrays have integer data types, the result is implementation-dependent, as type promotion between data type "kinds" (e.g., integer versus floating-point) is unspecified.\n\n   Specification-compliant libraries may choose to raise an error or return an array containing the element-wise results. If an array is returned, the array must have a real-valued floating-point data type.\n\nParameters\n----------\nx1: array\n    dividend input array. Should have a numeric data type.\nx2: array\n    divisor input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.\n- If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``-0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``-0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is ``+0``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is ``+infinity``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is ``-infinity``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is ``-infinity``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is ``+infinity``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``-infinity``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``-infinity``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``+infinity``.\n- If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``+0``.\n- If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``-0``.\n- If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``-0``.\n- If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``+0``.\n- If ``x1_i`` and ``x2_i`` have the same mathematical sign and are both nonzero finite numbers, the result has a positive mathematical sign.\n- If ``x1_i`` and ``x2_i`` have different mathematical signs and are both nonzero finite numbers, the result has a negative mathematical sign.\n- In the remaining cases, where neither ``-infinity``, ``+0``, ``-0``, nor ``NaN`` is involved, the quotient must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported rounding mode. If the magnitude is too large to represent, the operation overflows and the result is an ``infinity`` of appropriate mathematical sign. If the magnitude is too small to represent, the operation underflows and the result is a zero of appropriate mathematical sign.\n\nFor complex floating-point operands, division is defined according to the following table. For real components ``a`` and ``c`` and imaginary components ``b`` and ``d``,\n\n+------------+----------------+-----------------+--------------------------+\n|            | c              | dj              | c + dj                   |\n+============+================+=================+==========================+\n| **a**      | a / c          | -(a/d)j         | special rules            |\n+------------+----------------+-----------------+--------------------------+\n| **bj**     | (b/c)j         | b/d             | special rules            |\n+------------+----------------+-----------------+--------------------------+\n| **a + bj** | (a/c) + (b/c)j | b/d - (a/d)j    | special rules            |\n+------------+----------------+-----------------+--------------------------+\n\nIn general, for complex floating-point operands, real-valued floating-point special cases must independently apply to the real and imaginary component operations involving real numbers as described in the above table.\n\nWhen ``a``, ``b``, ``c``, or ``d`` are all finite numbers (i.e., a value other than ``NaN``, ``+infinity``, or ``-infinity``), division of complex floating-point operands should be computed as if calculated according to the textbook formula for complex number division\n\n.. math::\n   \\frac{a + bj}{c + dj} = \\frac{(ac + bd) + (bc - ad)j}{c^2 + d^2}\n\nWhen at least one of ``a``, ``b``, ``c``, or ``d`` is ``NaN``, ``+infinity``, or ``-infinity``,\n\n- If ``a``, ``b``, ``c``, and ``d`` are all ``NaN``, the result is ``NaN + NaN j``.\n- In the remaining cases, the result is implementation dependent.\n\n.. note::\n   For complex floating-point operands, the results of special cases may be implementation dependent depending on how an implementation chooses to model complex numbers and complex infinity (e.g., complex plane versus Riemann sphere). For those implementations following C99 and its one-infinity model, when at least one component is infinite, even if the other component is ``NaN``, the complex value is infinite, and the usual arithmetic rules do not apply to complex-complex division. In the interest of performance, other implementations may want to avoid the complex branching logic necessary to implement the one-infinity model and choose to implement all complex-complex division according to the textbook formula. Accordingly, special case behavior is unlikely to be consistent across implementations.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.'
    equal: equal[TArray,]
    "Computes the truth value of ``x1_i == x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. May have any data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). May have any data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x1_i`` is ``NaN`` or ``x2_i`` is ``NaN``, the result is ``False``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``+infinity``, the result is ``True``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``-infinity``, the result is ``True``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``True``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``True``.\n- If ``x1_i`` is a finite number, ``x2_i`` is a finite number, and ``x1_i`` equals ``x2_i``, the result is ``True``.\n- In the remaining cases, the result is ``False``.\n\nFor complex floating-point operands, let ``a = real(x1_i)``, ``b = imag(x1_i)``, ``c = real(x2_i)``, ``d = imag(x2_i)``, and\n\n- If ``a``, ``b``, ``c``, or ``d`` is ``NaN``, the result is ``False``.\n- In the remaining cases, the result is the logical AND of the equality comparison between the real values ``a`` and ``c`` (real components) and between the real values ``b`` and ``d`` (imaginary components), as described above for real-valued floating-point operands (i.e., ``a == c AND b == d``).\n\n.. note::\n   For discussion of complex number equality, see :ref:`complex-numbers`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    exp: exp[TArray,]
    "Calculates an implementation-dependent approximation to the exponential function for each element ``x_i`` of the input array ``x`` (``e`` raised to the power of ``x_i``, where ``e`` is the base of the natural logarithm).\n\n.. note::\n   For complex floating-point operands, ``exp(conj(x))`` must equal ``conj(exp(x))``.\n\n.. note::\n   The exponential function is an entire function in the complex plane and has no branch cuts.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated exponential function result for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``1``.\n- If ``x_i`` is ``-0``, the result is ``1``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``+0``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``1 + 0j``.\n- If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``infinity + 0j``.\n- If ``a`` is ``-infinity`` and ``b`` is a finite number, the result is ``+0 * cis(b)``.\n- If ``a`` is ``+infinity`` and ``b`` is a nonzero finite number, the result is ``+infinity * cis(b)``.\n- If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``0 + 0j`` (signs of real and imaginary components are unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``infinity + NaN j`` (sign of real component is unspecified).\n- If ``a`` is ``-infinity`` and ``b`` is ``NaN``, the result is ``0 + 0j`` (signs of real and imaginary components are unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``infinity + NaN j`` (sign of real component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.\n- If ``a`` is ``NaN`` and ``b`` is not equal to ``0``, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\nwhere ``cis(v)`` is ``cos(v) + sin(v)*1j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    expm1: expm1[TArray,]
    "Calculates an implementation-dependent approximation to ``exp(x)-1`` for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   The purpose of this function is to calculate ``exp(x)-1.0`` more accurately when `x` is close to zero. Accordingly, conforming implementations should avoid implementing this function as simply ``exp(x)-1.0``. See FDLIBM, or some other IEEE 754-2019 compliant mathematical library, for a potential reference implementation.\n\n.. note::\n   For complex floating-point operands, ``expm1(conj(x))`` must equal ``conj(expm1(x))``.\n\n.. note::\n   The exponential function is an entire function in the complex plane and has no branch cuts.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-1``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``0 + 0j``.\n- If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.\n- If ``a`` is ``-infinity`` and ``b`` is a finite number, the result is ``+0 * cis(b) - 1.0``.\n- If ``a`` is ``+infinity`` and ``b`` is a nonzero finite number, the result is ``+infinity * cis(b) - 1.0``.\n- If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``-1 + 0j`` (sign of imaginary component is unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``infinity + NaN j`` (sign of real component is unspecified).\n- If ``a`` is ``-infinity`` and ``b`` is ``NaN``, the result is ``-1 + 0j`` (sign of imaginary component is unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``infinity + NaN j`` (sign of real component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.\n- If ``a`` is ``NaN`` and ``b`` is not equal to ``0``, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\nwhere ``cis(v)`` is ``cos(v) + sin(v)*1j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    floor: floor[TArray,]
    "Rounds each element ``x_i`` of the input array ``x`` to the greatest (i.e., closest to ``+infinity``) integer-valued number that is not greater than ``x_i``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n**Special cases**\n\n- If ``x_i`` is already integer-valued, the result is ``x_i``.\n\nFor floating-point operands,\n\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-infinity``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``NaN``, the result is ``NaN``."
    floor_divide: floor_divide[TArray,]
    'Rounds the result of dividing each element ``x1_i`` of the input array ``x1`` by the respective element ``x2_i`` of the input array ``x2`` to the greatest (i.e., closest to `+infinity`) integer-value number that is not greater than the division result.\n\n.. note::\n   For input arrays which promote to an integer data type, the result of division by zero is unspecified and thus implementation-defined.\n\nParameters\n----------\nx1: array\n    dividend input array. Should have a real-valued data type.\nx2: array\n    divisor input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\n.. note::\n   Floor division was introduced in Python via `PEP 238 <https://www.python.org/dev/peps/pep-0238/>`_ with the goal to disambiguate "true division" (i.e., computing an approximation to the mathematical operation of division) from "floor division" (i.e., rounding the result of division toward negative infinity). The former was computed when one of the operands was a ``float``, while the latter was computed when both operands were ``int``\\s. Overloading the ``/`` operator to support both behaviors led to subtle numerical bugs when integers are possible, but not expected.\n\n   To resolve this ambiguity, ``/`` was designated for true division, and ``//`` was designated for floor division. Semantically, floor division was `defined <https://www.python.org/dev/peps/pep-0238/#semantics-of-floor-division>`_ as equivalent to ``a // b == floor(a/b)``; however, special floating-point cases were left ill-defined.\n\n   Accordingly, floor division is not implemented consistently across array libraries for some of the special cases documented below. Namely, when one of the operands is ``infinity``, libraries may diverge with some choosing to strictly follow ``floor(a/b)`` and others choosing to pair ``//`` with ``%`` according to the relation ``b = a % b + b * (a // b)``. The special cases leading to divergent behavior are documented below.\n\n   This specification prefers floor division to match ``floor(divide(x1, x2))`` in order to avoid surprising and unexpected results; however, array libraries may choose to more strictly follow Python behavior.\n\nFor floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.\n- If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``-0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``-0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is ``+0``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is ``+infinity``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is ``-infinity``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is ``-infinity``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is ``+infinity``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``-infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``-infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``+infinity``. (**note**: libraries may return ``NaN`` to match Python behavior.)\n- If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``+0``.\n- If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``-0``. (**note**: libraries may return ``-1.0`` to match Python behavior.)\n- If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``-0``. (**note**: libraries may return ``-1.0`` to match Python behavior.)\n- If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``+0``.\n- If ``x1_i`` and ``x2_i`` have the same mathematical sign and are both nonzero finite numbers, the result has a positive mathematical sign.\n- If ``x1_i`` and ``x2_i`` have different mathematical signs and are both nonzero finite numbers, the result has a negative mathematical sign.\n- In the remaining cases, where neither ``-infinity``, ``+0``, ``-0``, nor ``NaN`` is involved, the quotient must be computed and rounded to the greatest (i.e., closest to `+infinity`) representable integer-value number that is not greater than the division result. If the magnitude is too large to represent, the operation overflows and the result is an ``infinity`` of appropriate mathematical sign. If the magnitude is too small to represent, the operation underflows and the result is a zero of appropriate mathematical sign.'
    greater: greater[TArray,]
    "Computes the truth value of ``x1_i > x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx1: array\n    first input array. Should have a real-valued data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    greater_equal: greater_equal[TArray,]
    "Computes the truth value of ``x1_i >= x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx1: array\n    first input array. Should have a real-valued data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    hypot: hypot[TArray,]
    "Computes the square root of the sum of squares for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   The value computed by this function may be interpreted as the length of the hypotenuse of a right-angled triangle with sides of length ``x1_i`` and ``x2_i``, the distance of a point ``(x1_i, x2_i)`` from the origin ``(0, 0)``, or the magnitude of a complex number ``x1_i + x2_i * 1j``.\n\nParameters\n----------\nx1: array\n   first input array. Should have a real-valued floating-point data type.\nx2: array\n   second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.\n\nReturns\n-------\nout: array\n   an array containing the element-wise results. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\nThe purpose of this function is to avoid underflow and overflow during intermediate stages of computation. Accordingly, conforming implementations should not use naive implementations.\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x1_i`` is ``+infinity`` or ``-infinity`` and ``x2_i`` is any value, including ``NaN``, the result is ``+infinity``.\n- If ``x2_i`` is ``+infinity`` or ``-infinity`` and ``x1_i`` is any value, including ``NaN``, the result is ``+infinity``.\n- If ``x1_i`` is either ``+0`` or ``-0``, the result is equivalent to ``abs(x2_i)``.\n- If ``x2_i`` is either ``+0`` or ``-0``, the result is equivalent to ``abs(x1_i)``.\n- If ``x1_i`` is a finite number or ``NaN`` and ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x2_i`` is a finite number or ``NaN`` and ``x1_i`` is ``NaN``, the result is ``NaN``.\n- Underflow may only occur when both arguments are subnormal and the correct result is also subnormal.\n\nFor real-valued floating-point operands, ``hypot(x1, x2)`` must equal ``hypot(x2, x1)``, ``hypot(x1, -x2)``, ``hypot(-x1, x2)``, and ``hypot(-x1, -x2)``.\n\n.. note::\n   IEEE 754-2019 requires support for subnormal (a.k.a., denormal) numbers, which are useful for supporting gradual underflow. However, hardware support for subnormal numbers is not universal, and many platforms (e.g., accelerators) and compilers support toggling denormals-are-zero (DAZ) and/or flush-to-zero (FTZ) behavior to increase performance and to guard against timing attacks.\n\n   Accordingly, conforming implementations may vary in their support for subnormal numbers.\n\n.. versionadded:: 2023.12"
    imag: imag[TArray,]
    "Returns the imaginary component of a complex number for each element ``x_i`` of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a floating-point data type with the same floating-point precision as ``x`` (e.g., if ``x`` is ``complex64``, the returned array must have the floating-point data type ``float32``).\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    isfinite: isfinite[TArray,]
    "Tests each element ``x_i`` of the input array ``x`` to determine if finite.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing test results. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``False``.\n- If ``x_i`` is ``NaN``, the result is ``False``.\n- If ``x_i`` is a finite number, the result is ``True``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is ``NaN`` or ``b`` is ``NaN``, the result is ``False``.\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is any value, the result is ``False``.\n- If ``a`` is any value and ``b`` is either ``+infinity`` or ``-infinity``, the result is ``False``.\n- If ``a`` is a finite number and ``b`` is a finite number, the result is ``True``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    isinf: isinf[TArray,]
    "Tests each element ``x_i`` of the input array ``x`` to determine if equal to positive or negative infinity.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing test results. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``True``.\n- In the remaining cases, the result is ``False``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is any value (including ``NaN``), the result is ``True``.\n- If ``a`` is either a finite number or ``NaN`` and ``b`` is either ``+infinity`` or ``-infinity``, the result is ``True``.\n- In the remaining cases, the result is ``False``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    isnan: isnan[TArray,]
    "Tests each element ``x_i`` of the input array ``x`` to determine whether the element is ``NaN``.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing test results. The returned array should have a data type of ``bool``.\n\nNotes\n-----\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``True``.\n- In the remaining cases, the result is ``False``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` or ``b`` is ``NaN``, the result is ``True``.\n- In the remaining cases, the result is ``False``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    less: less[TArray,]
    "Computes the truth value of ``x1_i < x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx1: array\n    first input array. Should have a real-valued data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    less_equal: less_equal[TArray,]
    "Computes the truth value of ``x1_i <= x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx1: array\n    first input array. Should have a real-valued data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    log: log[TArray,]
    "Calculates an implementation-dependent approximation to the natural (base ``e``) logarithm for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   The natural logarithm of a complex number :math:`z` with polar coordinates :math:`(r,\\theta)` equals :math:`\\ln r + (\\theta + 2n\\pi)j` with principal value :math:`\\ln r + \\theta j`.\n\n.. note::\n   For complex floating-point operands, ``log(conj(x))`` must equal ``conj(log(x))``.\n\n.. note::\n   By convention, the branch cut of the natural logarithm is the negative real axis :math:`(-\\infty, 0)`.\n\n   The natural logarithm is a continuous function from above the branch cut, taking into account the sign of the imaginary component.\n\n   Accordingly, for complex arguments, the function returns the natural logarithm in the range of a strip in the interval :math:`[-\\pi j, +\\pi j]` along the imaginary axis and mathematically unbounded along the real axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated natural logarithm for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``0``, the result is ``NaN``.\n- If ``x_i`` is either ``+0`` or ``-0``, the result is ``-infinity``.\n- If ``x_i`` is ``1``, the result is ``+0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is ``-0`` and ``b`` is ``+0``, the result is ``-infinity + πj``.\n- If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``-infinity + 0j``.\n- If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + πj``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.\n- If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + 3πj/4``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    log1p: log1p[TArray,]
    "Calculates an implementation-dependent approximation to ``log(1+x)``, where ``log`` refers to the natural (base ``e``) logarithm, for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   The purpose of this function is to calculate ``log(1+x)`` more accurately when `x` is close to zero. Accordingly, conforming implementations should avoid implementing this function as simply ``log(1+x)``. See FDLIBM, or some other IEEE 754-2019 compliant mathematical library, for a potential reference implementation.\n\n.. note::\n   For complex floating-point operands, ``log1p(conj(x))`` must equal ``conj(log1p(x))``.\n\n.. note::\n   By convention, the branch cut of the natural logarithm is the negative real axis :math:`(-\\infty, 0)`.\n\n   The natural logarithm is a continuous function from above the branch cut, taking into account the sign of the imaginary component.\n\n   Accordingly, for complex arguments, the function returns the natural logarithm in the range of a strip in the interval :math:`[-\\pi j, +\\pi j]` along the imaginary axis and mathematically unbounded along the real axis.\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``-1``, the result is ``NaN``.\n- If ``x_i`` is ``-1``, the result is ``-infinity``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is ``-1`` and ``b`` is ``+0``, the result is ``-infinity + 0j``.\n- If ``a`` is a finite number and ``b`` is ``+infinity``, the result is ``+infinity + πj/2``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + πj``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+infinity + 0j``.\n- If ``a`` is ``-infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + 3πj/4``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``+infinity + πj/4``.\n- If ``a`` is either ``+infinity`` or ``-infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is a finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``+infinity``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    log2: log2[TArray,]
    "Calculates an implementation-dependent approximation to the base ``2`` logarithm for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   For complex floating-point operands, ``log2(conj(x))`` must equal ``conj(log2(x))``.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated base ``2`` logarithm for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``0``, the result is ``NaN``.\n- If ``x_i`` is either ``+0`` or ``-0``, the result is ``-infinity``.\n- If ``x_i`` is ``1``, the result is ``+0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented using the standard change of base formula\n\n.. math::\n   \\log_{2} x = \\frac{\\log_{e} x}{\\log_{e} 2}\n\nwhere :math:`\\log_{e}` is the natural logarithm, as implemented by :func:`~array_api.log`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    log10: log10[TArray,]
    "Calculates an implementation-dependent approximation to the base ``10`` logarithm for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   For complex floating-point operands, ``log10(conj(x))`` must equal ``conj(log10(x))``.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated base ``10`` logarithm for each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``0``, the result is ``NaN``.\n- If ``x_i`` is either ``+0`` or ``-0``, the result is ``-infinity``.\n- If ``x_i`` is ``1``, the result is ``+0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented using the standard change of base formula\n\n.. math::\n   \\log_{10} x = \\frac{\\log_{e} x}{\\log_{e} 10}\n\nwhere :math:`\\log_{e}` is the natural logarithm, as implemented by :func:`~array_api.log`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    logaddexp: logaddexp[TArray,]
    "Calculates the logarithm of the sum of exponentiations ``log(exp(x1) + exp(x2))`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. Should have a real-valued floating-point data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is not ``NaN``, the result is ``+infinity``.\n- If ``x1_i`` is not ``NaN`` and ``x2_i`` is ``+infinity``, the result is ``+infinity``."
    logical_and: logical_and[TArray,]
    "Computes the logical AND for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.\n\nParameters\n----------\nx1: array\n    first input array. Should have a boolean data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of `bool`."
    logical_not: logical_not[TArray,]
    "Computes the logical NOT for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.\n\nParameters\n----------\nx: array\n    input array. Should have a boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    logical_or: logical_or[TArray,]
    "Computes the logical OR for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.\n\nParameters\n----------\nx1: array\n    first input array. Should have a boolean data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    logical_xor: logical_xor[TArray,]
    "Computes the logical XOR for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   While this specification recommends that this function only accept input arrays having a boolean data type, specification-compliant array libraries may choose to accept input arrays having real-valued data types. If non-boolean data types are supported, zeros must be considered the equivalent of ``False``, while non-zeros must be considered the equivalent of ``True``.\n\nParameters\n----------\nx1: array\n    first input array. Should have a boolean data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a boolean data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``."
    maximum: maximum[TArray,]
    "Computes the maximum value for each element ``x1_i`` of the input array ``x1`` relative to the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n   first input array. Should have a real-valued data type.\nx2: array\n   second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n   an array containing the element-wise maximum values. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\nThe order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a maximum value, specification-compliant libraries may choose to return either value.\n\nFor backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).\n\n**Special Cases**\n\nFor floating-point operands,\n\n-   If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n\n.. versionadded:: 2023.12"
    minimum: minimum[TArray,]
    "Computes the minimum value for each element ``x1_i`` of the input array ``x1`` relative to the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n   first input array. Should have a real-valued data type.\nx2: array\n   second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n   an array containing the element-wise minimum values. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\nThe order of signed zeros is unspecified and thus implementation-defined. When choosing between ``-0`` or ``+0`` as a minimum value, specification-compliant libraries may choose to return either value.\n\nFor backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-defined (see :ref:`complex-number-ordering`).\n\n**Special Cases**\n\nFor floating-point operands,\n\n-   If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n\n.. versionadded:: 2023.12"
    multiply: multiply[TArray,]
    'Calculates the product for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   Floating-point multiplication is not always associative due to finite precision.\n\nParameters\n----------\nx1: array\n    first input array. Should have a numeric data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise products. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.\n- If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.\n- If ``x1_i`` and ``x2_i`` have the same mathematical sign, the result has a positive mathematical sign, unless the result is ``NaN``. If the result is ``NaN``, the "sign" of ``NaN`` is implementation-defined.\n- If ``x1_i`` and ``x2_i`` have different mathematical signs, the result has a negative mathematical sign, unless the result is ``NaN``. If the result is ``NaN``, the "sign" of ``NaN`` is implementation-defined.\n- If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is a signed infinity with the mathematical sign determined by the rule already stated above.\n- If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is a nonzero finite number, the result is a signed infinity with the mathematical sign determined by the rule already stated above.\n- If ``x1_i`` is a nonzero finite number and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is a signed infinity with the mathematical sign determined by the rule already stated above.\n- In the remaining cases, where neither ``infinity`` nor ``NaN`` is involved, the product must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported rounding mode. If the magnitude is too large to represent, the result is an `infinity` of appropriate mathematical sign. If the magnitude is too small to represent, the result is a zero of appropriate mathematical sign.\n\nFor complex floating-point operands, multiplication is defined according to the following table. For real components ``a`` and ``c`` and imaginary components ``b`` and ``d``,\n\n+------------+----------------+-----------------+--------------------------+\n|            | c              | dj              | c + dj                   |\n+============+================+=================+==========================+\n| **a**      | a * c          | (a*d)j          | (a*c) + (a*d)j           |\n+------------+----------------+-----------------+--------------------------+\n| **bj**     | (b*c)j         | -(b*d)          | -(b*d) + (b*c)j          |\n+------------+----------------+-----------------+--------------------------+\n| **a + bj** | (a*c) + (b*c)j | -(b*d) + (a*d)j | special rules            |\n+------------+----------------+-----------------+--------------------------+\n\nIn general, for complex floating-point operands, real-valued floating-point special cases must independently apply to the real and imaginary component operations involving real numbers as described in the above table.\n\nWhen ``a``, ``b``, ``c``, or ``d`` are all finite numbers (i.e., a value other than ``NaN``, ``+infinity``, or ``-infinity``), multiplication of complex floating-point operands should be computed as if calculated according to the textbook formula for complex number multiplication\n\n.. math::\n   (a + bj) \\cdot (c + dj) = (ac - bd) + (bc + ad)j\n\nWhen at least one of ``a``, ``b``, ``c``, or ``d`` is ``NaN``, ``+infinity``, or ``-infinity``,\n\n- If ``a``, ``b``, ``c``, and ``d`` are all ``NaN``, the result is ``NaN + NaN j``.\n- In the remaining cases, the result is implementation dependent.\n\n.. note::\n   For complex floating-point operands, the results of special cases may be implementation dependent depending on how an implementation chooses to model complex numbers and complex infinity (e.g., complex plane versus Riemann sphere). For those implementations following C99 and its one-infinity model, when at least one component is infinite, even if the other component is ``NaN``, the complex value is infinite, and the usual arithmetic rules do not apply to complex-complex multiplication. In the interest of performance, other implementations may want to avoid the complex branching logic necessary to implement the one-infinity model and choose to implement all complex-complex multiplication according to the textbook formula. Accordingly, special case behavior is unlikely to be consistent across implementations.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.'
    negative: negative[TArray,]
    "Computes the numerical negative of each element ``x_i`` (i.e., ``y_i = -x_i``) of the input array ``x``.\n\n.. note::\n   For signed integer data types, the numerical negative of the minimum representable integer is implementation-dependent.\n\n.. note::\n   If ``x`` has a complex floating-point data type, both the real and imaginary components for each ``x_i`` must be negated (a result which follows from the rules of complex number multiplication).\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    not_equal: not_equal[TArray,]
    "Computes the truth value of ``x1_i != x2_i`` for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nParameters\n----------\nx1: array\n    first input array. May have any data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`).\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If ``x1_i`` is ``NaN`` or ``x2_i`` is ``NaN``, the result is ``True``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is ``-infinity``, the result is ``True``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is ``+infinity``, the result is ``True``.\n- If ``x1_i`` is a finite number, ``x2_i`` is a finite number, and ``x1_i`` does not equal ``x2_i``, the result is ``True``.\n- In the remaining cases, the result is ``False``.\n\nFor complex floating-point operands, let ``a = real(x1_i)``, ``b = imag(x1_i)``, ``c = real(x2_i)``, ``d = imag(x2_i)``, and\n\n- If ``a``, ``b``, ``c``, or ``d`` is ``NaN``, the result is ``True``.\n- In the remaining cases, the result is the logical OR of the equality comparison between the real values ``a`` and ``c`` (real components) and between the real values ``b`` and ``d`` (imaginary components), as described above for real-valued floating-point operands (i.e., ``a != c OR b != d``).\n\n.. note::\n   For discussion of complex number equality, see :ref:`complex-numbers`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    positive: positive[TArray,]
    "Computes the numerical positive of each element ``x_i`` (i.e., ``y_i = +x_i``) of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    pow: pow[TArray,]
    'Calculates an implementation-dependent approximation of exponentiation by raising each element ``x1_i`` (the base) of the input array ``x1`` to the power of ``x2_i`` (the exponent), where ``x2_i`` is the corresponding element of the input array ``x2``.\n\n.. note::\n   If both ``x1`` and ``x2`` have integer data types, the result of ``pow`` when ``x2_i`` is negative (i.e., less than zero) is unspecified and thus implementation-dependent.\n\n   If ``x1`` has an integer data type and ``x2`` has a floating-point data type, behavior is implementation-dependent (type promotion between data type "kinds" (integer versus floating-point) is unspecified).\n\n.. note::\n   By convention, the branch cut of the natural logarithm is the negative real axis :math:`(-\\infty, 0)`.\n\n   The natural logarithm is a continuous function from above the branch cut, taking into account the sign of the imaginary component. As special cases involving complex floating-point operands should be handled according to ``exp(x2*log(x1))``, exponentiation has the same branch cut for ``x1`` as the natural logarithm (see :func:`~array_api.log`).\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx1: array\n    first input array whose elements correspond to the exponentiation base. Should have a numeric data type.\nx2: array\n    second input array whose elements correspond to the exponentiation exponent. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x1_i`` is not equal to ``1`` and ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x2_i`` is ``+0``, the result is ``1``, even if ``x1_i`` is ``NaN``.\n- If ``x2_i`` is ``-0``, the result is ``1``, even if ``x1_i`` is ``NaN``.\n- If ``x1_i`` is ``NaN`` and ``x2_i`` is not equal to ``0``, the result is ``NaN``.\n- If ``abs(x1_i)`` is greater than ``1`` and ``x2_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``abs(x1_i)`` is greater than ``1`` and ``x2_i`` is ``-infinity``, the result is ``+0``.\n- If ``abs(x1_i)`` is ``1`` and ``x2_i`` is ``+infinity``, the result is ``1``.\n- If ``abs(x1_i)`` is ``1`` and ``x2_i`` is ``-infinity``, the result is ``1``.\n- If ``x1_i`` is ``1`` and ``x2_i`` is not ``NaN``, the result is ``1``.\n- If ``abs(x1_i)`` is less than ``1`` and ``x2_i`` is ``+infinity``, the result is ``+0``.\n- If ``abs(x1_i)`` is less than ``1`` and ``x2_i`` is ``-infinity``, the result is ``+infinity``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is greater than ``0``, the result is ``+infinity``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is less than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``-infinity``, ``x2_i`` is greater than ``0``, and ``x2_i`` is an odd integer value, the result is ``-infinity``.\n- If ``x1_i`` is ``-infinity``, ``x2_i`` is greater than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+infinity``.\n- If ``x1_i`` is ``-infinity``, ``x2_i`` is less than ``0``, and ``x2_i`` is an odd integer value, the result is ``-0``.\n- If ``x1_i`` is ``-infinity``, ``x2_i`` is less than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``+infinity``.\n- If ``x1_i`` is ``-0``, ``x2_i`` is greater than ``0``, and ``x2_i`` is an odd integer value, the result is ``-0``.\n- If ``x1_i`` is ``-0``, ``x2_i`` is greater than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+0``.\n- If ``x1_i`` is ``-0``, ``x2_i`` is less than ``0``, and ``x2_i`` is an odd integer value, the result is ``-infinity``.\n- If ``x1_i`` is ``-0``, ``x2_i`` is less than ``0``, and ``x2_i`` is not an odd integer value, the result is ``+infinity``.\n- If ``x1_i`` is less than ``0``, ``x1_i`` is a finite number, ``x2_i`` is a finite number, and ``x2_i`` is not an integer value, the result is ``NaN``.\n\nFor complex floating-point operands, special cases should be handled as if the operation is implemented as ``exp(x2*log(x1))``.\n\n.. note::\n   Conforming implementations are allowed to treat special cases involving complex floating-point operands more carefully than as described in this specification.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.'
    real: real[TArray,]
    "Returns the real component of a complex number for each element ``x_i`` of the input array ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. The returned array must have a floating-point data type with the same floating-point precision as ``x`` (e.g., if ``x`` is ``complex64``, the returned array must have the floating-point data type ``float32``).\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    remainder: remainder[TArray,]
    "Returns the remainder of division for each element ``x1_i`` of the input array ``x1`` and the respective element ``x2_i`` of the input array ``x2``.\n\n.. note::\n   This function is equivalent to the Python modulus operator ``x1_i % x2_i``.\n\n.. note::\n   For input arrays which promote to an integer data type, the result of division by zero is unspecified and thus implementation-defined.\n\nParameters\n----------\nx1: array\n    dividend input array. Should have a real-valued data type.\nx2: array\n    divisor input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise results. Each element-wise result must have the same sign as the respective element ``x2_i``. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\n.. note::\n   In general, similar to Python's ``%`` operator, this function is **not** recommended for floating-point operands as semantics do not follow IEEE 754. That this function is specified to accept floating-point operands is primarily for reasons of backward compatibility.\n\nFor floating-point operands,\n\n- If either ``x1_i`` or ``x2_i`` is ``NaN``, the result is ``NaN``.\n- If ``x1_i`` is either ``+infinity`` or ``-infinity`` and ``x2_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.\n- If ``x1_i`` is either ``+0`` or ``-0`` and ``x2_i`` is either ``+0`` or ``-0``, the result is ``NaN``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is greater than ``0``, the result is ``+0``.\n- If ``x1_i`` is ``+0`` and ``x2_i`` is less than ``0``, the result is ``-0``.\n- If ``x1_i`` is ``-0`` and ``x2_i`` is less than ``0``, the result is ``-0``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``+0``, the result is ``NaN``.\n- If ``x1_i`` is greater than ``0`` and ``x2_i`` is ``-0``, the result is ``NaN``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``+0``, the result is ``NaN``.\n- If ``x1_i`` is less than ``0`` and ``x2_i`` is ``-0``, the result is ``NaN``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``NaN``.\n- If ``x1_i`` is ``+infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``NaN``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``NaN``.\n- If ``x1_i`` is ``-infinity`` and ``x2_i`` is a negative (i.e., less than ``0``) finite number, the result is ``NaN``.\n- If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``x1_i``. (**note**: this result matches Python behavior.)\n- If ``x1_i`` is a positive (i.e., greater than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``x2_i``. (**note**: this result matches Python behavior.)\n- If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``+infinity``, the result is ``x2_i``. (**note**: this results matches Python behavior.)\n- If ``x1_i`` is a negative (i.e., less than ``0``) finite number and ``x2_i`` is ``-infinity``, the result is ``x1_i``. (**note**: this result matches Python behavior.)\n- In the remaining cases, the result must match that of the Python ``%`` operator."
    round: round[TArray,]
    "Rounds each element ``x_i`` of the input array ``x`` to the nearest integer-valued number.\n\n.. note::\n   For complex floating-point operands, real and imaginary components must be independently rounded to the nearest integer-valued number.\n\n   Rounded real and imaginary components must be equal to their equivalent rounded real-valued floating-point counterparts (i.e., for complex-valued ``x``, ``real(round(x))`` must equal ``round(real(x)))`` and ``imag(round(x))`` must equal ``round(imag(x))``).\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n**Special cases**\n\n.. note::\n   For complex floating-point operands, the following special cases apply to real and imaginary components independently (e.g., if ``real(x_i)`` is ``NaN``, the rounded real component is ``NaN``).\n\n- If ``x_i`` is already integer-valued, the result is ``x_i``.\n\nFor floating-point operands,\n\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-infinity``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If two integers are equally close to ``x_i``, the result is the even integer closest to ``x_i``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    sign: sign[TArray,]
    "Returns an indication of the sign of a number for each element ``x_i`` of the input array ``x``.\n\nThe sign function (also known as the **signum function**) of a number :math:`x_i` is defined as\n\n.. math::\n   \\operatorname{sign}(x_i) = \\begin{cases}\n   0 & \\textrm{if } x_i = 0 \\\\\n   \\frac{x_i}{|x_i|} & \\textrm{otherwise}\n   \\end{cases}\n\nwhere :math:`|x_i|` is the absolute value of :math:`x_i`.\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued operands,\n\n- If ``x_i`` is less than ``0``, the result is ``-1``.\n- If ``x_i`` is either ``-0`` or ``+0``, the result is ``0``.\n- If ``x_i`` is greater than ``0``, the result is ``+1``.\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``-0`` or ``+0`` and ``b`` is either ``-0`` or ``+0``, the result is ``0 + 0j``.\n- If ``a`` is ``NaN`` or ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- In the remaining cases, special cases must be handled according to the rules of complex number division (see :func:`~array_api.divide`).\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    signbit: signbit[TArray,]
    "Determines whether the sign bit is set for each element ``x_i`` of the input array ``x``.\n\nThe sign bit of a real-valued floating-point number ``x_i`` is set whenever ``x_i`` is either ``-0``, less than zero, or a signed ``NaN`` (i.e., a ``NaN`` value whose sign bit is ``1``).\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``+0``, the result is ``False``.\n- If ``x_i`` is ``-0``, the result is ``True``.\n- If ``x_i`` is ``+infinity``, the result is ``False``.\n- If ``x_i`` is ``-infinity``, the result is ``True``.\n- If ``x_i`` is a positive (i.e., greater than ``0``) finite number, the result is ``False``.\n- If ``x_i`` is a negative (i.e., less than ``0``) finite number, the result is ``True``.\n- If ``x_i`` is ``NaN`` and the sign bit of ``x_i`` is ``0``, the result is ``False``.\n- If ``x_i`` is ``NaN`` and the sign bit of ``x_i`` is ``1``, the result is ``True``.\n\n.. versionadded:: 2023.12"
    sin: sin[TArray,]
    "Calculates an implementation-dependent approximation to the sine for each element ``x_i`` of the input array ``x``.\n\nEach element ``x_i`` is assumed to be expressed in radians.\n\n.. note::\n   The sine is an entire function on the complex plane and has no branch cuts.\n\n.. note::\n   For complex arguments, the mathematical definition of sine is\n\n   .. math::\n      \\begin{align} \\operatorname{sin}(x) &= \\frac{e^{jx} - e^{-jx}}{2j} \\\\ &= \\frac{\\operatorname{sinh}(jx)}{j} \\\\ &= \\frac{\\operatorname{sinh}(jx)}{j} \\cdot \\frac{j}{j} \\\\ &= -j \\cdot \\operatorname{sinh}(jx) \\end{align}\n\n   where :math:`\\operatorname{sinh}` is the hyperbolic sine.\n\nParameters\n----------\nx: array\n    input array whose elements are each expressed in radians. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * sinh(x*1j)``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    sinh: sinh[TArray,]
    "Calculates an implementation-dependent approximation to the hyperbolic sine for each element ``x_i`` of the input array ``x``.\n\nThe mathematical definition of the hyperbolic sine is\n\n.. math::\n   \\operatorname{sinh}(x) = \\frac{e^x - e^{-x}}{2}\n\n.. note::\n   The hyperbolic sine is an entire function in the complex plane and has no branch cuts. The function is periodic, with period :math:`2\\pi j`, with respect to the imaginary component.\n\nParameters\n----------\nx: array\n    input array whose elements each represent a hyperbolic angle. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the hyperbolic sine of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\n.. note::\n   For all operands, ``sinh(x)`` must equal ``-sinh(-x)``.\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n.. note::\n   For complex floating-point operands, ``sinh(conj(x))`` must equal ``conj(sinh(x))``.\n\n- If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.\n- If ``a`` is ``+0`` and ``b`` is ``+infinity``, the result is ``0 + NaN j`` (sign of the real component is unspecified).\n- If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``0 + NaN j`` (sign of the real component is unspecified).\n- If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.\n- If ``a`` is a positive (i.e., greater than ``0``) finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+0``, the result is ``+infinity + 0j``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive finite number, the result is ``+infinity * cis(b)``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``infinity + NaN j`` (sign of the real component is unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``infinity + NaN j`` (sign of the real component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.\n- If ``a`` is ``NaN`` and ``b`` is a nonzero finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\nwhere ``cis(v)`` is ``cos(v) + sin(v)*1j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    square: square[TArray,]
    "Squares each element ``x_i`` of the input array ``x``.\n\nThe square of a number ``x_i`` is defined as\n\n.. math::\n   x_i^2 = x_i \\cdot x_i\n\nParameters\n----------\nx: array\n    input array. Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the evaluated result for each element in ``x``. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor floating-point operands, special cases must be handled as if the operation is implemented as ``x * x`` (see :func:`~array_api.multiply`).\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    sqrt: sqrt[TArray,]
    "Calculates the principal square root for each element ``x_i`` of the input array ``x``.\n\n.. note::\n   After rounding, each result must be indistinguishable from the infinitely precise result (as required by IEEE 754).\n\n.. note::\n   For complex floating-point operands, ``sqrt(conj(x))`` must equal ``conj(sqrt(x))``.\n\n.. note::\n   By convention, the branch cut of the square root is the negative real axis :math:`(-\\infty, 0)`.\n\n   The square root is a continuous function from above the branch cut, taking into account the sign of the imaginary component.\n\n   Accordingly, for complex arguments, the function returns the square root in the range of the right half-plane, including the imaginary axis (i.e., the plane defined by :math:`[0, +\\infty)` along the real axis and :math:`(-\\infty, +\\infty)` along the imaginary axis).\n\n   *Note: branch cuts follow C99 and have provisional status* (see :ref:`branch-cuts`).\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the square root of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is less than ``0``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n- If ``a`` is either ``+0`` or ``-0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.\n- If ``a`` is any value (including ``NaN``) and ``b`` is ``+infinity``, the result is ``+infinity + infinity j``.\n- If ``a`` is a finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` ``-infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``NaN + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``+0 + infinity j``.\n- If ``a`` is ``-infinity`` and ``b`` is ``NaN``, the result is ``NaN + infinity j`` (sign of the imaginary component is unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``+infinity + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is any value, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    subtract: subtract[TArray,]
    "Calculates the difference for each element ``x1_i`` of the input array ``x1`` with the respective element ``x2_i`` of the input array ``x2``.\n\nThe result of ``x1_i - x2_i`` must be the same as ``x1_i + (-x2_i)`` and must be governed by the same floating-point rules as addition (see :meth:`add`).\n\nParameters\n----------\nx1: array\n    first input array. Should have a numeric data type.\nx2: array\n    second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`). Should have a numeric data type.\n\nReturns\n-------\nout: array\n    an array containing the element-wise differences. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    tan: tan[TArray,]
    "Calculates an implementation-dependent approximation to the tangent for each element ``x_i`` of the input array ``x``.\n\nEach element ``x_i`` is assumed to be expressed in radians.\n\n.. note::\n   Tangent is an analytical function on the complex plane and has no branch cuts. The function is periodic, with period :math:`\\pi j`, with respect to the real component and has first order poles along the real line at coordinates :math:`(\\pi (\\frac{1}{2} + n), 0)`. However, IEEE 754 binary floating-point representation cannot represent the value :math:`\\pi / 2` exactly, and, thus, no argument value is possible for which a pole error occurs.\n\n.. note::\n   For complex arguments, the mathematical definition of tangent is\n\n   .. math::\n      \\begin{align} \\operatorname{tan}(x) &= \\frac{j(e^{-jx} - e^{jx})}{e^{-jx} + e^{jx}} \\\\ &= (-1) \\frac{j(e^{jx} - e^{-jx})}{e^{jx} + e^{-jx}} \\\\ &= -j \\cdot \\operatorname{tanh}(jx) \\end{align}\n\n   where :math:`\\operatorname{tanh}` is the hyperbolic tangent.\n\nParameters\n----------\nx: array\n    input array whose elements are expressed in radians. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.\n\nFor complex floating-point operands, special cases must be handled as if the operation is implemented as ``-1j * tanh(x*1j)``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    tanh: tanh[TArray,]
    "Calculates an implementation-dependent approximation to the hyperbolic tangent for each element ``x_i`` of the input array ``x``.\n\nThe mathematical definition of the hyperbolic tangent is\n\n.. math::\n   \\begin{align} \\operatorname{tanh}(x) &= \\frac{\\operatorname{sinh}(x)}{\\operatorname{cosh}(x)} \\\\ &= \\frac{e^x - e^{-x}}{e^x + e^{-x}} \\end{align}\n\nwhere :math:`\\operatorname{sinh}(x)` is the hyperbolic sine and :math:`\\operatorname{cosh}(x)` is the hyperbolic cosine.\n\n.. note::\n   The hyperbolic tangent is an analytical function on the complex plane and has no branch cuts. The function is periodic, with period :math:`\\pi j`, with respect to the imaginary component and has first order poles along the imaginary line at coordinates :math:`(0, \\pi (\\frac{1}{2} + n))`. However, IEEE 754 binary floating-point representation cannot represent :math:`\\pi / 2` exactly, and, thus, no argument value is possible such that a pole error occurs.\n\nParameters\n----------\nx: array\n    input array whose elements each represent a hyperbolic angle. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the hyperbolic tangent of each element in ``x``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Special cases**\n\n.. note::\n   For all operands, ``tanh(-x)`` must equal ``-tanh(x)``.\n\nFor real-valued floating-point operands,\n\n- If ``x_i`` is ``NaN``, the result is ``NaN``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``+infinity``, the result is ``+1``.\n- If ``x_i`` is ``-infinity``, the result is ``-1``.\n\nFor complex floating-point operands, let ``a = real(x_i)``, ``b = imag(x_i)``, and\n\n.. note::\n   For complex floating-point operands, ``tanh(conj(x))`` must equal ``conj(tanh(x))``.\n\n- If ``a`` is ``+0`` and ``b`` is ``+0``, the result is ``+0 + 0j``.\n- If ``a`` is a nonzero finite number and ``b`` is ``+infinity``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+0`` and ``b`` is ``+infinity``, the result is ``+0 + NaN j``.\n- If ``a`` is a nonzero finite number and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n- If ``a`` is ``+0`` and ``b`` is ``NaN``, the result is ``+0 + NaN j``.\n- If ``a`` is ``+infinity`` and ``b`` is a positive (i.e., greater than ``0``) finite number, the result is ``1 + 0j``.\n- If ``a`` is ``+infinity`` and ``b`` is ``+infinity``, the result is ``1 + 0j`` (sign of the imaginary component is unspecified).\n- If ``a`` is ``+infinity`` and ``b`` is ``NaN``, the result is ``1 + 0j`` (sign of the imaginary component is unspecified).\n- If ``a`` is ``NaN`` and ``b`` is ``+0``, the result is ``NaN + 0j``.\n- If ``a`` is ``NaN`` and ``b`` is a nonzero number, the result is ``NaN + NaN j``.\n- If ``a`` is ``NaN`` and ``b`` is ``NaN``, the result is ``NaN + NaN j``.\n\n.. warning::\n   For historical reasons stemming from the C standard, array libraries may not return the expected result when ``a`` is ``+0`` and ``b`` is either ``+infinity`` or ``NaN``. The result should be ``+0 + NaN j`` in both cases; however, for libraries compiled against older C versions, the result may be ``NaN + NaN j``.\n\n   Array libraries are not required to patch these older C versions, and, thus, users are advised that results may vary across array library implementations for these special cases.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    trunc: trunc[TArray,]
    "Rounds each element ``x_i`` of the input array ``x`` to the nearest integer-valued number that is closer to zero than ``x_i``.\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\n\nReturns\n-------\nout: array\n    an array containing the rounded result for each element in ``x``. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n**Special cases**\n\n- If ``x_i`` is already integer-valued, the result is ``x_i``.\n\nFor floating-point operands,\n\n- If ``x_i`` is ``+infinity``, the result is ``+infinity``.\n- If ``x_i`` is ``-infinity``, the result is ``-infinity``.\n- If ``x_i`` is ``+0``, the result is ``+0``.\n- If ``x_i`` is ``-0``, the result is ``-0``.\n- If ``x_i`` is ``NaN``, the result is ``NaN``."
    argmax: argmax[TArray,]
    "Returns the indices of the maximum values along a specified axis.\n\nWhen the maximum value occurs multiple times, only the indices corresponding to the first occurrence are returned.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\naxis: Optional[int]\n    axis along which to search. If ``None``, the function must return the index of the maximum value of the flattened array. Default: ``None``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if ``axis`` is ``None``, a zero-dimensional array containing the index of the first occurrence of the maximum value; otherwise, a non-zero-dimensional array containing the indices of the maximum values. The returned array must have be the default array index data type."
    argmin: argmin[TArray,]
    "Returns the indices of the minimum values along a specified axis.\n\nWhen the minimum value occurs multiple times, only the indices corresponding to the first occurrence are returned.\n\n.. note::\n   For backward compatibility, conforming implementations may support complex numbers; however, inequality comparison of complex numbers is unspecified and thus implementation-dependent (see :ref:`complex-number-ordering`).\n\nParameters\n----------\nx: array\n    input array. Should have a real-valued data type.\naxis: Optional[int]\n    axis along which to search. If ``None``, the function must return the index of the minimum value of the flattened array. Default: ``None``.\nkeepdims: bool\n    if ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if ``axis`` is ``None``, a zero-dimensional array containing the index of the first occurrence of the minimum value; otherwise, a non-zero-dimensional array containing the indices of the minimum values. The returned array must have the default array index data type."
    nonzero: nonzero[TArray,]
    "Returns the indices of the array elements which are non-zero.\n\n.. note::\n   If ``x`` has a complex floating-point data type, non-zero elements are those elements having at least one component (real or imaginary) which is non-zero.\n\n.. note::\n   If ``x`` has a boolean data type, non-zero elements are those elements which are equal to ``True``.\n\n.. admonition:: Data-dependent output shape\n   :class: admonition important\n\n   The shape of the output array for this function depends on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.\n\nParameters\n----------\nx: array\n    input array. Must have a positive rank. If ``x`` is zero-dimensional, the function must raise an exception.\n\nReturns\n-------\nout: Tuple[array, ...]\n    a tuple of ``k`` arrays, one for each dimension of ``x`` and each of size ``n`` (where ``n`` is the total number of non-zero elements), containing the indices of the non-zero elements in that dimension. The indices must be returned in row-major, C-style order. The returned array must have the default array index data type.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    searchsorted: searchsorted[TArray,]
    "Finds the indices into ``x1`` such that, if the corresponding elements in ``x2`` were inserted before the indices, the order of ``x1``, when sorted in ascending order, would be preserved.\n\nParameters\n----------\nx1: array\n    input array. Must be a one-dimensional array. Should have a real-valued data type. If ``sorter`` is ``None``, must be sorted in ascending order; otherwise, ``sorter`` must be an array of indices that sort ``x1`` in ascending order.\nx2: array\n    array containing search values. Should have a real-valued data type.\nside: Literal['left', 'right']\n    argument controlling which index is returned if a value lands exactly on an edge.\n\n    Let ``v`` be an element of ``x2`` given by ``v = x2[j]``, where ``j`` refers to a valid index (see :ref:`indexing`).\n\n    - If ``v`` is less than all elements in ``x1``, then ``out[j]`` must be ``0``.\n    - If ``v`` is greater than all elements in ``x1``, then ``out[j]`` must be ``M``, where ``M`` is the number of elements in ``x1``.\n    - Otherwise, each returned index ``i = out[j]`` must satisfy an index condition:\n\n      - If ``side == 'left'``, then ``x1[i-1] < v <= x1[i]``.\n      - If ``side == 'right'``, then ``x1[i-1] <= v < x1[i]``.\n\n    Default: ``'left'``.\nsorter: Optional[array]\n    array of indices that sort ``x1`` in ascending order. The array must have the same shape as ``x1`` and have an integer data type. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array of indices with the same shape as ``x2``. The returned array must have the default array index data type.\n\nNotes\n-----\n\nFor real-valued floating-point arrays, the sort order of NaNs and signed zeros is unspecified and thus implementation-dependent. Accordingly, when a real-valued floating-point array contains NaNs and signed zeros, what constitutes ascending order may vary among specification-conforming array libraries.\n\nWhile behavior for arrays containing NaNs and signed zeros is implementation-dependent, specification-conforming libraries should, however, ensure consistency with ``sort`` and ``argsort`` (i.e., if a value in ``x2`` is inserted into ``x1`` according to the corresponding index in the output array and ``sort`` is invoked on the resultant array, the sorted result should be an array in the same order).\n\n.. versionadded:: 2023.12"
    where: where[TArray,]
    "Returns elements chosen from ``x1`` or ``x2`` depending on ``condition``.\n\nParameters\n----------\ncondition: array\n    when ``True``, yield ``x1_i``; otherwise, yield ``x2_i``. Should have a boolean data type. Must be compatible with ``x1`` and ``x2`` (see :ref:`broadcasting`).\nx1: array\n    first input array. Must be compatible with ``condition`` and ``x2`` (see :ref:`broadcasting`).\nx2: array\n    second input array. Must be compatible with ``condition`` and ``x1`` (see :ref:`broadcasting`).\n\nReturns\n-------\nout: array\n    an array with elements from ``x1`` where ``condition`` is ``True``, and elements from ``x2`` elsewhere. The returned array must have a data type determined by :ref:`type-promotion` rules with the arrays ``x1`` and ``x2``."
    all: all[TArray,]
    "Tests whether all input array elements evaluate to ``True`` along a specified axis.\n\n.. note::\n   Positive infinity, negative infinity, and NaN must evaluate to ``True``.\n\n.. note::\n   If ``x`` has a complex floating-point data type, elements having a non-zero component (real or imaginary) must evaluate to ``True``.\n\n.. note::\n   If ``x`` is an empty array or the size of the axis (dimension) along which to evaluate elements is zero, the test result must be ``True``.\n\nParameters\n----------\nx: array\n    input array.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which to perform a logical AND reduction. By default, a logical AND reduction must be performed over the entire array. If a tuple of integers, logical AND reductions must be performed over multiple axes. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to perform a reduction by counting backward from the last dimension (where ``-1`` refers to the last dimension). If provided an invalid ``axis``, the function must raise an exception. Default: ``None``.\nkeepdims: bool\n    If ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if a logical AND reduction was performed over the entire array, the returned array must be a zero-dimensional array containing the test result; otherwise, the returned array must be a non-zero-dimensional array containing the test results. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    any: any[TArray,]
    "Tests whether any input array element evaluates to ``True`` along a specified axis.\n\n.. note::\n   Positive infinity, negative infinity, and NaN must evaluate to ``True``.\n\n.. note::\n   If ``x`` has a complex floating-point data type, elements having a non-zero component (real or imaginary) must evaluate to ``True``.\n\n.. note::\n   If ``x`` is an empty array or the size of the axis (dimension) along which to evaluate elements is zero, the test result must be ``False``.\n\nParameters\n----------\nx: array\n    input array.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis or axes along which to perform a logical OR reduction. By default, a logical OR reduction must be performed over the entire array. If a tuple of integers, logical OR reductions must be performed over multiple axes. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to perform a reduction by counting backward from the last dimension (where ``-1`` refers to the last dimension). If provided an invalid ``axis``, the function must raise an exception. Default: ``None``.\nkeepdims: bool\n    If ``True``, the reduced axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes (dimensions) must not be included in the result. Default: ``False``.\n\nReturns\n-------\nout: array\n    if a logical OR reduction was performed over the entire array, the returned array must be a zero-dimensional array containing the test result; otherwise, the returned array must be a non-zero-dimensional array containing the test results. The returned array must have a data type of ``bool``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    __array_namespace_info__: __array_namespace_info__[TDevice,]
    "Returns a namespace with Array API namespace inspection utilities.\n\nSee :ref:`inspection` for a list of inspection APIs.\n\nReturns\n-------\nout: Info\n    An object containing Array API namespace inspection utilities.\n\nNotes\n-----\n\nThe returned object may be either a namespace or a class, so long as an Array API user can access inspection utilities as follows:\n\n::\n\n  info = xp.__array_namespace_info__()\n  info.capabilities()\n  info.devices()\n  info.dtypes()\n  info.default_dtypes()\n  # ...\n\n.. versionadded: 2023.12"
    take: take[TArray,]
    "Returns elements of an array along an axis.\n\n.. note::\n   Conceptually, ``take(x, indices, axis=3)`` is equivalent to ``x[:,:,:,indices,...]``; however, explicit indexing via arrays of indices is not currently supported in this specification due to concerns regarding ``__setitem__`` and array mutation semantics.\n\nParameters\n----------\nx: array\n    input array.\nindices: array\n    array indices. The array must be one-dimensional and have an integer data type.\n\n    .. note::\n       This specification does not require bounds checking. The behavior for out-of-bounds indices is left unspecified.\n\naxis: Optional[int]\n    axis over which to select values. If ``axis`` is negative, the function must determine the axis along which to select values by counting from the last dimension.\n\n    If ``x`` is a one-dimensional array, providing an ``axis`` is optional; however, if ``x`` has more than one dimension, providing an ``axis`` is required.\n\nReturns\n-------\nout: array\n    an array having the same data type as ``x``. The output array must have the same rank (i.e., number of dimensions) as ``x`` and must have the same shape as ``x``, except for the axis specified by ``axis`` whose size must equal the number of elements in ``indices``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Out-of-bounds behavior is explicitly left unspecified."
    matmul: matmul[TArray,]
    "Computes the matrix product.\n\n.. note::\n   The ``matmul`` function must implement the same semantics as the built-in ``@`` operator (see `PEP 465 <https://www.python.org/dev/peps/pep-0465>`_).\n\nParameters\n----------\nx1: array\n    first input array. Should have a numeric data type. Must have at least one dimension. If ``x1`` is one-dimensional having shape ``(M,)`` and ``x2`` has more than one dimension, ``x1`` must be promoted to a two-dimensional array by prepending ``1`` to its dimensions (i.e., must have shape ``(1, M)``). After matrix multiplication, the prepended dimensions in the returned array must be removed. If ``x1`` has more than one dimension (including after vector-to-matrix promotion), ``shape(x1)[:-2]`` must be compatible with ``shape(x2)[:-2]`` (after vector-to-matrix promotion) (see :ref:`broadcasting`). If ``x1`` has shape ``(..., M, K)``, the innermost two dimensions form matrices on which to perform matrix multiplication.\nx2: array\n    second input array. Should have a numeric data type. Must have at least one dimension. If ``x2`` is one-dimensional having shape ``(N,)`` and ``x1`` has more than one dimension, ``x2`` must be promoted to a two-dimensional array by appending ``1`` to its dimensions (i.e., must have shape ``(N, 1)``). After matrix multiplication, the appended dimensions in the returned array must be removed. If ``x2`` has more than one dimension (including after vector-to-matrix promotion), ``shape(x2)[:-2]`` must be compatible with ``shape(x1)[:-2]`` (after vector-to-matrix promotion) (see :ref:`broadcasting`). If ``x2`` has shape ``(..., K, N)``, the innermost two dimensions form matrices on which to perform matrix multiplication.\n\n\n.. note::\n   If either ``x1`` or ``x2`` has a complex floating-point data type, neither argument must be complex-conjugated or transposed. If conjugation and/or transposition is desired, these operations should be explicitly performed prior to computing the matrix product.\n\nReturns\n-------\nout: array\n    -   if both ``x1`` and ``x2`` are one-dimensional arrays having shape ``(N,)``, a zero-dimensional array containing the inner product as its only element.\n    -   if ``x1`` is a two-dimensional array having shape ``(M, K)`` and ``x2`` is a two-dimensional array having shape ``(K, N)``, a two-dimensional array containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ and having shape ``(M, N)``.\n    -   if ``x1`` is a one-dimensional array having shape ``(K,)`` and ``x2`` is an array having shape ``(..., K, N)``, an array having shape ``(..., N)`` (i.e., prepended dimensions during vector-to-matrix promotion must be removed) and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_.\n    -   if ``x1`` is an array having shape ``(..., M, K)`` and ``x2`` is a one-dimensional array having shape ``(K,)``, an array having shape ``(..., M)`` (i.e., appended dimensions during vector-to-matrix promotion must be removed) and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_.\n    -   if ``x1`` is a two-dimensional array having shape ``(M, K)`` and ``x2`` is an array having shape ``(..., K, N)``, an array having shape ``(..., M, N)`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.\n    -   if ``x1`` is an array having shape ``(..., M, K)`` and ``x2`` is a two-dimensional array having shape ``(K, N)``, an array having shape ``(..., M, N)`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.\n    -   if either ``x1`` or ``x2`` has more than two dimensions, an array having a shape determined by :ref:`broadcasting` ``shape(x1)[:-2]`` against ``shape(x2)[:-2]`` and containing the `conventional matrix product <https://en.wikipedia.org/wiki/Matrix_multiplication>`_ for each stacked matrix.\n\n    The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n**Raises**\n\n-   if either ``x1`` or ``x2`` is a zero-dimensional array.\n-   if ``x1`` is a one-dimensional array having shape ``(K,)``, ``x2`` is a one-dimensional array having shape ``(L,)``, and ``K != L``.\n-   if ``x1`` is a one-dimensional array having shape ``(K,)``, ``x2`` is an array having shape ``(..., L, N)``, and ``K != L``.\n-   if ``x1`` is an array having shape ``(..., M, K)``, ``x2`` is a one-dimensional array having shape ``(L,)``, and ``K != L``.\n-   if ``x1`` is an array having shape ``(..., M, K)``, ``x2`` is an array having shape ``(..., L, N)``, and ``K != L``."
    matrix_transpose: matrix_transpose[TArray,]
    "Transposes a matrix (or a stack of matrices) ``x``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.\n\nReturns\n-------\nout: array\n    an array containing the transpose for each matrix and having shape ``(..., N, M)``. The returned array must have the same data type as ``x``."
    tensordot: tensordot[TArray,]
    "Returns a tensor contraction of ``x1`` and ``x2`` over specific axes.\n\n.. note::\n   The ``tensordot`` function corresponds to the generalized matrix product.\n\nParameters\n----------\nx1: array\n    first input array. Should have a numeric data type.\nx2: array\n    second input array. Should have a numeric data type. Corresponding contracted axes of ``x1`` and ``x2`` must be equal.\n\n    .. note::\n       Contracted axes (dimensions) must not be broadcasted.\n\naxes: Union[int, Tuple[Sequence[int], Sequence[int]]]\n    number of axes (dimensions) to contract or explicit sequences of axis (dimension) indices for ``x1`` and ``x2``, respectively.\n\n    If ``axes`` is an ``int`` equal to ``N``, then contraction must be performed over the last ``N`` axes of ``x1`` and the first ``N`` axes of ``x2`` in order. The size of each corresponding axis (dimension) must match. Must be nonnegative.\n\n    -   If ``N`` equals ``0``, the result is the tensor (outer) product.\n    -   If ``N`` equals ``1``, the result is the tensor dot product.\n    -   If ``N`` equals ``2``, the result is the tensor double contraction (default).\n\n    If ``axes`` is a tuple of two sequences ``(x1_axes, x2_axes)``, the first sequence must apply to ``x1`` and the second sequence to ``x2``. Both sequences must have the same length. Each axis (dimension) ``x1_axes[i]`` for ``x1`` must have the same size as the respective axis (dimension) ``x2_axes[i]`` for ``x2``. Each index referred to in a sequence must be unique. If ``x1`` has rank (i.e, number of dimensions) ``N``, a valid ``x1`` axis must reside on the half-open interval ``[-N, N)``. If ``x2`` has rank ``M``, a valid ``x2`` axis must reside on the half-open interval ``[-M, M)``.\n\n\n.. note::\n   If either ``x1`` or ``x2`` has a complex floating-point data type, neither argument must be complex-conjugated or transposed. If conjugation and/or transposition is desired, these operations should be explicitly performed prior to computing the generalized matrix product.\n\nReturns\n-------\nout: array\n    an array containing the tensor contraction whose shape consists of the non-contracted axes (dimensions) of the first array ``x1``, followed by the non-contracted axes (dimensions) of the second array ``x2``. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Allow negative axes."
    vecdot: vecdot[TArray,]
    "Computes the (vector) dot product of two arrays.\n\nLet :math:`\\mathbf{a}` be a vector in ``x1`` and :math:`\\mathbf{b}` be a corresponding vector in ``x2``. The dot product is defined as\n\n.. math::\n   \\mathbf{a} \\cdot \\mathbf{b} = \\sum_{i=0}^{n-1} \\overline{a_i}b_i\n\nover the dimension specified by ``axis`` and where :math:`n` is the dimension size and :math:`\\overline{a_i}` denotes the complex conjugate if :math:`a_i` is complex and the identity if :math:`a_i` is real-valued.\n\nParameters\n----------\nx1: array\n    first input array. Should have a floating-point data type.\nx2: array\n    second input array. Must be compatible with ``x1`` for all non-contracted axes (see :ref:`broadcasting`). The size of the axis over which to compute the dot product must be the same size as the respective axis in ``x1``. Should have a floating-point data type.\n\n    .. note::\n       The contracted axis (dimension) must not be broadcasted.\n\naxis: int\n    the axis (dimension) of ``x1`` and ``x2`` containing the vectors for which to compute the dot product. Should be an integer on the interval ``[-N, -1]``, where ``N`` is ``min(x1.ndim, x2.ndim)``. The function must determine the axis along which to compute the dot product by counting backward from the last dimension (where ``-1`` refers to the last dimension). By default, the function must compute the dot product over the last axis. Default: ``-1``.\n\nReturns\n-------\nout: array\n    if ``x1`` and ``x2`` are both one-dimensional arrays, a zero-dimensional containing the dot product; otherwise, a non-zero-dimensional array containing the dot products and having rank ``N-1``, where ``N`` is the rank (number of dimensions) of the shape determined according to :ref:`broadcasting` along the non-contracted axes. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n**Raises**\n\n-   if the size of the axis over which to compute the dot product is not the same (before broadcasting) for both ``x1`` and ``x2``.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Restricted ``axis`` to only negative integers."
    broadcast_arrays: broadcast_arrays[TArray,]
    "Broadcasts one or more arrays against one another.\n\nParameters\n----------\narrays: array\n    an arbitrary number of to-be broadcasted arrays.\n\nReturns\n-------\nout: List[array]\n    a list of broadcasted arrays. Each array must have the same shape. Each array must have the same dtype as its corresponding input array."
    broadcast_to: broadcast_to[TArray,]
    "Broadcasts an array to a specified shape.\n\nParameters\n----------\nx: array\n    array to broadcast.\nshape: Tuple[int, ...]\n    array shape. Must be compatible with ``x`` (see :ref:`broadcasting`). If the array is incompatible with the specified shape, the function should raise an exception.\n\nReturns\n-------\nout: array\n    an array having a specified shape. Must have the same data type as ``x``."
    concat: concat[TArray,]
    "Joins a sequence of arrays along an existing axis.\n\nParameters\n----------\narrays: Union[Tuple[array, ...], List[array]]\n    input arrays to join. The arrays must have the same shape, except in the dimension specified by ``axis``.\naxis: Optional[int]\n    axis along which the arrays will be joined. If ``axis`` is ``None``, arrays must be flattened before concatenation. If ``axis`` is negative, the function must determine the axis along which to join by counting from the last dimension. Default: ``0``.\n\nReturns\n-------\nout: array\n    an output array containing the concatenated values. If the input arrays have different data types, normal :ref:`type-promotion` must apply. If the input arrays have the same data type, the output array must have the same data type as the input arrays.\n\n    .. note::\n       This specification leaves type promotion between data type families (i.e., ``intxx`` and ``floatxx``) unspecified."
    expand_dims: expand_dims[TArray,]
    "Expands the shape of an array by inserting a new axis (dimension) of size one at the position specified by ``axis``.\n\nParameters\n----------\nx: array\n    input array.\naxis: int\n    axis position (zero-based). If ``x`` has rank (i.e, number of dimensions) ``N``, a valid ``axis`` must reside on the closed-interval ``[-N-1, N]``. If provided a negative ``axis``, the axis position at which to insert a singleton dimension must be computed as ``N + axis + 1``. Hence, if provided ``-1``, the resolved axis position must be ``N`` (i.e., a singleton dimension must be appended to the input array ``x``). If provided ``-N-1``, the resolved axis position must be ``0`` (i.e., a singleton dimension must be prepended to the input array ``x``).\n\nReturns\n-------\nout: array\n    an expanded output array having the same data type as ``x``.\n\nRaises\n------\nIndexError\n    If provided an invalid ``axis`` position, an ``IndexError`` should be raised."
    flip: flip[TArray,]
    "Reverses the order of elements in an array along the given axis. The shape of the array must be preserved.\n\nParameters\n----------\nx: array\n    input array.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis (or axes) along which to flip. If ``axis`` is ``None``, the function must flip all input array axes. If ``axis`` is negative, the function must count from the last dimension. If provided more than one axis, the function must flip only the specified axes. Default: ``None``.\n\nReturns\n-------\nout: array\n    an output array having the same data type and shape as ``x`` and whose elements, relative to ``x``, are reordered."
    moveaxis: moveaxis[TArray,]
    "Moves array axes (dimensions) to new positions, while leaving other axes in their original positions.\n\nParameters\n----------\nx: array\n    input array.\nsource: Union[int, Tuple[int, ...]]\n    Axes to move. Provided axes must be unique. If ``x`` has rank (i.e, number of dimensions) ``N``, a valid axis must reside on the half-open interval ``[-N, N)``.\ndestination: Union[int, Tuple[int, ...]]\n    indices defining the desired positions for each respective ``source`` axis index. Provided indices must be unique. If ``x`` has rank (i.e, number of dimensions) ``N``, a valid axis must reside on the half-open interval ``[-N, N)``.\n\nReturns\n-------\nout: array\n    an array containing reordered axes. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n.. versionadded:: 2023.12"
    permute_dims: permute_dims[TArray,]
    "Permutes the axes (dimensions) of an array ``x``.\n\nParameters\n----------\nx: array\n    input array.\naxes: Tuple[int, ...]\n    tuple containing a permutation of ``(0, 1, ..., N-1)`` where ``N`` is the number of axes (dimensions) of ``x``.\n\nReturns\n-------\nout: array\n    an array containing the axes permutation. The returned array must have the same data type as ``x``."
    repeat: repeat[TArray,]
    "Repeats each element of an array a specified number of times on a per-element basis.\n\n.. admonition:: Data-dependent output shape\n    :class: important\n\n    When ``repeats`` is an array, the shape of the output array for this function depends on the data values in the ``repeats`` array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing the values in ``repeats``. Accordingly, such libraries may choose to omit support for ``repeats`` arrays; however, conforming implementations must support providing a literal ``int``. See :ref:`data-dependent-output-shapes` section for more details.\n\nParameters\n----------\nx: array\n    input array containing elements to repeat.\nrepeats: Union[int, array]\n    the number of repetitions for each element.\n\n    If ``axis`` is ``None``, let ``N = prod(x.shape)`` and\n\n    -   if ``repeats`` is an array, ``repeats`` must be broadcast compatible with the shape ``(N,)`` (i.e., be a one-dimensional array having shape ``(1,)`` or ``(N,)``).\n    -   if ``repeats`` is an integer, ``repeats`` must be broadcasted to the shape `(N,)`.\n\n    If ``axis`` is not ``None``, let ``M = x.shape[axis]`` and\n\n    -   if ``repeats`` is an array, ``repeats`` must be broadcast compatible with the shape ``(M,)`` (i.e., be a one-dimensional array having shape ``(1,)`` or ``(M,)``).\n    -   if ``repeats`` is an integer, ``repeats`` must be broadcasted to the shape ``(M,)``.\n\n    If ``repeats`` is an array, the array must have an integer data type.\n\n    .. note::\n       For specification-conforming array libraries supporting hardware acceleration, providing an array for ``repeats`` may cause device synchronization due to an unknown output shape. For those array libraries where synchronization concerns are applicable, conforming array libraries are advised to include a warning in their documentation regarding potential performance degradation when ``repeats`` is an array.\n\naxis: Optional[int]\n    the axis (dimension) along which to repeat elements. If ``axis`` is `None`, the function must flatten the input array ``x`` and then repeat elements of the flattened input array and return the result as a one-dimensional output array. A flattened input array must be flattened in row-major, C-style order. Default: ``None``.\n\nReturns\n-------\nout: array\n    an output array containing repeated elements. The returned array must have the same data type as ``x``. If ``axis`` is ``None``, the returned array must be a one-dimensional array; otherwise, the returned array must have the same shape as ``x``, except for the axis (dimension) along which elements were repeated.\n\nNotes\n-----\n\n.. versionadded:: 2023.12"
    reshape: reshape[TArray,]
    "Reshapes an array without changing its data.\n\nParameters\n----------\nx: array\n    input array to reshape.\nshape: Tuple[int, ...]\n    a new shape compatible with the original shape. One shape dimension is allowed to be ``-1``. When a shape dimension is ``-1``, the corresponding output array shape dimension must be inferred from the length of the array and the remaining dimensions.\ncopy: Optional[bool]\n    whether or not to copy the input array. If ``True``, the function must always copy. If ``False``, the function must never copy. If ``None``, the function must avoid copying, if possible, and may copy otherwise. Default: ``None``.\n\nReturns\n-------\nout: array\n    an output array having the same data type and elements as ``x``.\n\nRaises\n------\nValueError\n    If ``copy=False`` and a copy would be necessary, a ``ValueError``\n    should be raised."
    roll: roll[TArray,]
    "Rolls array elements along a specified axis. Array elements that roll beyond the last position are re-introduced at the first position. Array elements that roll beyond the first position are re-introduced at the last position.\n\nParameters\n----------\nx: array\n    input array.\nshift: Union[int, Tuple[int, ...]]\n    number of places by which the elements are shifted. If ``shift`` is a tuple, then ``axis`` must be a tuple of the same size, and each of the given axes must be shifted by the corresponding element in ``shift``. If ``shift`` is an ``int`` and ``axis`` a tuple, then the same ``shift`` must be used for all specified axes. If a shift is positive, then array elements must be shifted positively (toward larger indices) along the dimension of ``axis``. If a shift is negative, then array elements must be shifted negatively (toward smaller indices) along the dimension of ``axis``.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    axis (or axes) along which elements to shift. If ``axis`` is ``None``, the array must be flattened, shifted, and then restored to its original shape. Default: ``None``.\n\nReturns\n-------\nout: array\n    an output array having the same data type as ``x`` and whose elements, relative to ``x``, are shifted."
    squeeze: squeeze[TArray,]
    "Removes singleton dimensions (axes) from ``x``.\n\nParameters\n----------\nx: array\n    input array.\naxis: Union[int, Tuple[int, ...]]\n    axis (or axes) to squeeze.\n\nReturns\n-------\nout: array\n    an output array having the same data type and elements as ``x``.\n\nRaises\n------\nValueError\n    If a specified axis has a size greater than one (i.e., it is not a\n    singleton dimension), a ``ValueError`` should be raised."
    stack: stack[TArray,]
    "Joins a sequence of arrays along a new axis.\n\nParameters\n----------\narrays: Union[Tuple[array, ...], List[array]]\n    input arrays to join. Each array must have the same shape.\naxis: int\n    axis along which the arrays will be joined. Providing an ``axis`` specifies the index of the new axis in the dimensions of the result. For example, if ``axis`` is ``0``, the new axis will be the first dimension and the output array will have shape ``(N, A, B, C)``; if ``axis`` is ``1``, the new axis will be the second dimension and the output array will have shape ``(A, N, B, C)``; and, if ``axis`` is ``-1``, the new axis will be the last dimension and the output array will have shape ``(A, B, C, N)``. A valid ``axis`` must be on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If provided an ``axis`` outside of the required interval, the function must raise an exception. Default: ``0``.\n\nReturns\n-------\nout: array\n    an output array having rank ``N+1``, where ``N`` is the rank (number of dimensions) of ``x``. If the input arrays have different data types, normal :ref:`type-promotion` must apply. If the input arrays have the same data type, the output array must have the same data type as the input arrays.\n\n    .. note::\n       This specification leaves type promotion between data type families (i.e., ``intxx`` and ``floatxx``) unspecified."
    tile: tile[TArray,]
    "Constructs an array by tiling an input array.\n\nParameters\n----------\nx: array\n    input array.\nrepetitions: Tuple[int, ...]\n    number of repetitions along each axis (dimension).\n\n    Let ``N = len(x.shape)`` and ``M = len(repetitions)``.\n\n    If ``N > M``, the function must prepend ones until all axes (dimensions) are specified (e.g., if ``x`` has shape ``(8,6,4,2)`` and ``repetitions`` is the tuple ``(3,3)``, then ``repetitions`` must be treated as ``(1,1,3,3)``).\n\n    If ``N < M``, the function must prepend singleton axes (dimensions) to ``x`` until ``x`` has as many axes (dimensions) as ``repetitions`` specifies (e.g., if ``x`` has shape ``(4,2)`` and ``repetitions`` is the tuple ``(3,3,3,3)``, then ``x`` must be treated as if it has shape ``(1,1,4,2)``).\n\nReturns\n-------\nout: array\n    a tiled output array. The returned array must have the same data type as ``x`` and must have a rank (i.e., number of dimensions) equal to ``max(N, M)``. If ``S`` is the shape of the tiled array after prepending singleton dimensions (if necessary) and ``r`` is the tuple of repetitions after prepending ones (if necessary), then the number of elements along each axis (dimension) must satisfy ``S[i]*r[i]``, where ``i`` refers to the ``i`` th axis (dimension).\n\nNotes\n-----\n\n.. versionadded:: 2023.12"
    unstack: unstack[TArray,]
    "Splits an array into a sequence of arrays along the given axis.\n\nParameters\n----------\nx: array\n    input array.\naxis: int\n    axis along which the array will be split. A valid ``axis`` must be on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If provided an ``axis`` outside of the required interval, the function must raise an exception. Default: ``0``.\n\nReturns\n-------\nout: Tuple[array, ...]\n    tuple of slices along the given dimension. All the arrays have the same shape.\n\nNotes\n-----\n\n.. versionadded:: 2023.12"
    e: TArray
    "\nIEEE 754 floating-point representation of Euler's constant.\n\n``e = 2.71828182845904523536028747135266249775724709369995...``\n"
    inf: TArray
    "\nIEEE 754 floating-point representation of (positive) infinity.\n"
    nan: TArray
    "\nIEEE 754 floating-point representation of Not a Number (``NaN``).\n"
    newaxis: TArray
    "\nAn alias for ``None`` which is useful for indexing arrays.\n"
    pi: TArray
    "\nIEEE 754 floating-point representation of the mathematical constant ``π``.\n\n``pi = 3.1415926535897932384626433...``\n"
    unique_all: unique_all[TArray,]
    "Returns the unique elements of an input array ``x``, the first occurring indices for each unique element in ``x``, the indices from the set of unique elements that reconstruct ``x``, and the corresponding counts for each unique element in ``x``.\n\n.. admonition:: Data-dependent output shape\n    :class: important\n\n    The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.\n\n.. note::\n   Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.\n\n   -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.\n   -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.\n   -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).\n\n   As signed zeros are not distinct, using ``inverse_indices`` to reconstruct the input array is not guaranteed to return an array having the exact same values.\n\n   Each ``nan`` value and each complex floating-point value having a ``nan`` component should have a count of one, while the counts for signed zeros should be aggregated as a single count.\n\nParameters\n----------\nx: array\n    input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.\n\nReturns\n-------\nout: Tuple[array, array, array, array]\n    a namedtuple ``(values, indices, inverse_indices, counts)`` whose\n\n    - first element must have the field name ``values`` and must be a one-dimensional array containing the unique elements of ``x``. The array must have the same data type as ``x``.\n    - second element must have the field name ``indices`` and must be an array containing the indices (first occurrences) of a flattened ``x`` that result in ``values``. The array must have the same shape as ``values`` and must have the default array index data type.\n    - third element must have the field name ``inverse_indices`` and must be an array containing the indices of ``values`` that reconstruct ``x``. The array must have the same shape as ``x`` and must have the default array index data type.\n    - fourth element must have the field name ``counts`` and must be an array containing the number of times each unique element occurs in ``x``. The order of the returned counts must match the order of ``values``, such that a specific element in ``counts`` corresponds to the respective unique element in ``values``. The returned array must have same shape as ``values`` and must have the default array index data type.\n\n    .. note::\n       The order of unique elements is not specified and may vary between implementations.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Clarified flattening behavior and required the order of ``counts`` match the order of ``values``."
    unique_counts: unique_counts[TArray,]
    "Returns the unique elements of an input array ``x`` and the corresponding counts for each unique element in ``x``.\n\n.. admonition:: Data-dependent output shape\n    :class: important\n\n    The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.\n\n.. note::\n   Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.\n\n   -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.\n   -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.\n   -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).\n\n   Each ``nan`` value and each complex floating-point value having a ``nan`` component should have a count of one, while the counts for signed zeros should be aggregated as a single count.\n\nParameters\n----------\nx: array\n    input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.\n\nReturns\n-------\nout: Tuple[array, array]\n    a namedtuple `(values, counts)` whose\n\n    -   first element must have the field name ``values`` and must be a one-dimensional array containing the unique elements of ``x``. The array must have the same data type as ``x``.\n    -   second element must have the field name `counts` and must be an array containing the number of times each unique element occurs in ``x``. The order of the returned counts must match the order of ``values``, such that a specific element in ``counts`` corresponds to the respective unique element in ``values``. The returned array must have same shape as ``values`` and must have the default array index data type.\n\n    .. note::\n       The order of unique elements is not specified and may vary between implementations.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Clarified flattening behavior and required the order of ``counts`` match the order of ``values``."
    unique_inverse: unique_inverse[TArray,]
    "Returns the unique elements of an input array ``x`` and the indices from the set of unique elements that reconstruct ``x``.\n\n.. admonition:: Data-dependent output shape\n    :class: important\n\n    The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.\n\n.. note::\n   Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.\n\n   -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.\n   -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.\n   -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).\n\n   As signed zeros are not distinct, using ``inverse_indices`` to reconstruct the input array is not guaranteed to return an array having the exact same values.\n\nParameters\n----------\nx: array\n    input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.\n\nReturns\n-------\nout: Tuple[array, array]\n    a namedtuple ``(values, inverse_indices)`` whose\n\n    -   first element must have the field name ``values`` and must be a one-dimensional array containing the unique elements of ``x``. The array must have the same data type as ``x``.\n    -   second element must have the field name ``inverse_indices`` and must be an array containing the indices of ``values`` that reconstruct ``x``. The array must have the same shape as ``x`` and have the default array index data type.\n\n    .. note::\n       The order of unique elements is not specified and may vary between implementations.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Clarified flattening behavior."
    unique_values: unique_values[TArray,]
    "Returns the unique elements of an input array ``x``.\n\n.. admonition:: Data-dependent output shape\n    :class: important\n\n    The shapes of two of the output arrays for this function depend on the data values in the input array; hence, array libraries which build computation graphs (e.g., JAX, Dask, etc.) may find this function difficult to implement without knowing array values. Accordingly, such libraries may choose to omit this function. See :ref:`data-dependent-output-shapes` section for more details.\n\n.. note::\n   Uniqueness should be determined based on value equality (see :func:`~array_api.equal`). For input arrays having floating-point data types, value-based equality implies the following behavior.\n\n   -   As ``nan`` values compare as ``False``, ``nan`` values should be considered distinct.\n   -   As complex floating-point values having at least one ``nan`` component compare as ``False``, complex floating-point values having ``nan`` components should be considered distinct.\n   -   As ``-0`` and ``+0`` compare as ``True``, signed zeros should not be considered distinct, and the corresponding unique element will be implementation-dependent (e.g., an implementation could choose to return ``-0`` if ``-0`` occurs before ``+0``).\n\nParameters\n----------\nx: array\n    input array. If ``x`` has more than one dimension, the function must flatten ``x`` and return the unique elements of the flattened array.\n\nReturns\n-------\nout: array\n    a one-dimensional array containing the set of unique elements in ``x``. The returned array must have the same data type as ``x``.\n\n    .. note::\n       The order of unique elements is not specified and may vary between implementations.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Required that the output array must be one-dimensional."
    bool: TDtype
    complex128: TDtype
    complex64: TDtype
    float32: TDtype
    float64: TDtype
    int16: TDtype
    int32: TDtype
    int64: TDtype
    int8: TDtype
    uint16: TDtype
    uint32: TDtype
    uint64: TDtype
    uint8: TDtype
    Device: TDevice


@runtime_checkable
class LinalgNamespace[TArray: Array, TDtype](Protocol):
    cholesky: cholesky[TArray,]
    "Returns the lower (upper) Cholesky decomposition of a complex Hermitian or real symmetric positive-definite matrix ``x``.\n\nIf ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThe lower **Cholesky decomposition** of a complex Hermitian or real symmetric positive-definite matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as\n\n.. math::\n   x = LL^{H} \\qquad \\text{L $\\in\\ \\mathbb{K}^{n \\times n}$}\n\nwhere :math:`L` is a lower triangular matrix and :math:`L^{H}` is the conjugate transpose when :math:`L` is complex-valued and the transpose when :math:`L` is real-valued.\n\nThe upper Cholesky decomposition is defined similarly\n\n.. math::\n   x = U^{H}U \\qquad \\text{U $\\in\\ \\mathbb{K}^{n \\times n}$}\n\nwhere :math:`U` is an upper triangular matrix.\n\nWhen ``x`` is a stack of matrices, the function must compute the Cholesky decomposition for each matrix in the stack.\n\n.. note::\n   Whether an array library explicitly checks whether an input array is Hermitian or a symmetric positive-definite matrix (or a stack of matrices) is implementation-defined.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square complex Hermitian or real symmetric positive-definite matrices. Should have a floating-point data type.\nupper: bool\n    If ``True``, the result must be the upper-triangular Cholesky factor :math:`U`. If ``False``, the result must be the lower-triangular Cholesky factor :math:`L`. Default: ``False``.\n\nReturns\n-------\nout: array\n    an array containing the Cholesky factors for each square matrix. If ``upper`` is ``False``, the returned array must contain lower-triangular matrices; otherwise, the returned array must contain upper-triangular matrices. The returned array must have a floating-point data type determined by :ref:`type-promotion` and must have the same shape as ``x``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    cross: cross[TArray,]
    "Returns the cross product of 3-element vectors.\n\nIf ``x1`` and/or ``x2`` are multi-dimensional arrays (i.e., the broadcasted result has a rank greater than ``1``), then the cross-product of each pair of corresponding 3-element vectors is independently computed.\n\nParameters\n----------\nx1: array\n    first input array. Must have a numeric data type. The size of the axis over which the cross product is to be computed must be equal to 3.\nx2: array\n    second input array. Must be broadcast compatible with ``x1`` along all axes other than the axis along which the cross-product is computed (see :ref:`broadcasting`). The size of the axis over which the cross product is to be computed must be equal to 3. Must have a numeric data type.\n\n    .. note::\n       The compute axis (dimension) must not be broadcasted.\n\naxis: int\n    the axis (dimension) of ``x1`` and ``x2`` containing the vectors for which to compute the cross product. Should be an integer on the interval ``[-N, -1]``, where ``N`` is ``min(x1.ndim, x2.ndim)``. The function must determine the axis along which to compute the cross product by counting backward from the last dimension (where ``-1`` refers to the last dimension). By default, the function must compute the cross product over the last axis. Default: ``-1``.\n\nReturns\n-------\nout: array\n    an array containing the cross products. The returned array must have a data type determined by :ref:`type-promotion`.\n\n\nNotes\n-----\n\n**Raises**\n\n-   if the size of the axis over which to compute the cross product is not equal to ``3`` (before broadcasting) for both ``x1`` and ``x2``.\n\n.. versionchanged:: 2022.12\n   Added support for broadcasting.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Restricted broadcasting to only non-compute axes and required that ``axis`` be a negative integer."
    det: det[TArray,]
    "Returns the determinant of a square matrix (or a stack of square matrices) ``x``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    if ``x`` is a two-dimensional array, a zero-dimensional array containing the determinant; otherwise, a non-zero dimensional array containing the determinant for each square matrix. The returned array must have the same data type as ``x``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    diagonal: diagonal[TArray,]
    "Returns the specified diagonals of a matrix (or a stack of matrices) ``x``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices.\noffset: int\n    offset specifying the off-diagonal relative to the main diagonal.\n\n    - ``offset = 0``: the main diagonal.\n    - ``offset > 0``: off-diagonal above the main diagonal.\n    - ``offset < 0``: off-diagonal below the main diagonal.\n\n    Default: `0`.\n\nReturns\n-------\nout: array\n    an array containing the diagonals and whose shape is determined by removing the last two dimensions and appending a dimension equal to the size of the resulting diagonals. The returned array must have the same data type as ``x``."
    eigh: eigh[TArray,]
    "Returns an eigenvalue decomposition of a complex Hermitian or real symmetric matrix (or a stack of matrices) ``x``.\n\nIf ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThe **eigenvalue decomposition** of a complex Hermitian or real symmetric matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as\n\n.. math::\n   x = Q \\Lambda Q^H\n\nwith :math:`Q \\in \\mathbb{K}^{n \\times n}` and :math:`\\Lambda \\in \\mathbb{R}^n` and where :math:`Q^H` is the conjugate transpose when :math:`Q` is complex and the transpose when :math:`Q` is real-valued and :math:`\\Lambda` is a diagonal matrix whose diagonal elements are the corresponding eigenvalues. When ``x`` is real-valued, :math:`Q` is orthogonal, and, when ``x`` is complex, :math:`Q` is unitary.\n\n.. note::\n   The eigenvalues of a complex Hermitian or real symmetric matrix are always real.\n\n.. warning::\n   The eigenvectors of a symmetric matrix are not unique and are not continuous with respect to ``x``. Because eigenvectors are not unique, different hardware and software may compute different eigenvectors.\n\n   Non-uniqueness stems from the fact that multiplying an eigenvector by :math:`-1` when ``x`` is real-valued and by :math:`e^{\\phi j}` (:math:`\\phi \\in \\mathbb{R}`) when ``x`` is complex produces another set of valid eigenvectors.\n\n.. note::\n   Whether an array library explicitly checks whether an input array is Hermitian or a symmetric matrix (or a stack of matrices) is implementation-defined.\n\n.. note::\n   The function ``eig`` will be added in a future version of the specification.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.\n\nReturns\n-------\nout: Tuple[array, array]\n    a namedtuple (``eigenvalues``, ``eigenvectors``) whose\n\n    -   first element must have the field name ``eigenvalues`` (corresponding to :math:`\\operatorname{diag}\\Lambda` above) and must be an array consisting of computed eigenvalues. The array containing the eigenvalues must have shape ``(..., M)`` and must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then ``eigenvalues`` must be ``float64``).\n    -   second element have have the field name ``eigenvectors`` (corresponding to :math:`Q` above) and must be an array where the columns of the inner most matrices contain the computed eigenvectors. These matrices must be orthogonal. The array containing the eigenvectors must have shape ``(..., M, M)`` and must have the same data type as ``x``.\n\nNotes\n-----\n\n.. note::\n   Eigenvalue sort order is left unspecified and is thus implementation-dependent.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    eigvalsh: eigvalsh[TArray,]
    "Returns the eigenvalues of a complex Hermitian or real symmetric matrix (or a stack of matrices) ``x``.\n\nIf ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThe **eigenvalues** of a complex Hermitian or real symmetric matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` are defined as the roots (counted with multiplicity) of the polynomial :math:`p` of degree :math:`n` given by\n\n.. math::\n   p(\\lambda) = \\operatorname{det}(x - \\lambda I_n)\n\nwhere :math:`\\lambda \\in \\mathbb{R}` and where :math:`I_n` is the *n*-dimensional identity matrix.\n\n.. note:;\n   The eigenvalues of a complex Hermitian or real symmetric matrix are always real.\n\n.. note::\n   Whether an array library explicitly checks whether an input array is Hermitian or a symmetric matrix (or a stack of matrices) is implementation-defined.\n\n.. note::\n   The function ``eigvals`` will be added in a future version of the specification.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the computed eigenvalues. The returned array must have shape ``(..., M)`` and have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then must have a ``float64`` data type).\n\nNotes\n-----\n\n.. note::\n   Eigenvalue sort order is left unspecified and is thus implementation-dependent.\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    inv: inv[TArray,]
    "Returns the multiplicative inverse of a square matrix (or a stack of square matrices) ``x``.\n\nIf ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThe **inverse matrix** :math:`x^{-1} \\in\\ \\mathbb{K}^{n \\times n}` of a square matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as\n\n.. math::\n   x^{-1}x = xx^{-1} = I_n\n\nwhere :math:`I_n` is the *n*-dimensional identity matrix.\n\nThe inverse matrix exists if and only if ``x`` is invertible. When ``x`` is invertible, the inverse is unique.\n\nWhen ``x`` is a stack of matrices, the function must compute the inverse for each matrix in the stack.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the multiplicative inverses. The returned array must have a floating-point data type determined by :ref:`type-promotion` and must have the same shape as ``x``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    matmul: matmul[TArray,]
    "Alias for :func:`~array_api.matmul`."
    matrix_norm: matrix_norm[TArray,]
    "Computes the matrix norm of a matrix (or a stack of matrices) ``x``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a floating-point data type.\nkeepdims: bool\n    If ``True``, the last two axes (dimensions) must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the last two axes (dimensions) must not be included in the result. Default: ``False``.\nord: Optional[Union[int, float, Literal[inf, -inf, 'fro', 'nuc']]]\n    order of the norm. The following mathematical norms must be supported:\n\n    +------------------+---------------------------------+\n    | ord              | description                     |\n    +==================+=================================+\n    | 'fro'            | Frobenius norm                  |\n    +------------------+---------------------------------+\n    | 'nuc'            | nuclear norm                    |\n    +------------------+---------------------------------+\n    | 1                | max(sum(abs(x), axis=0))        |\n    +------------------+---------------------------------+\n    | 2                | largest singular value          |\n    +------------------+---------------------------------+\n    | inf              | max(sum(abs(x), axis=1))        |\n    +------------------+---------------------------------+\n\n    The following non-mathematical \"norms\" must be supported:\n\n    +------------------+---------------------------------+\n    | ord              | description                     |\n    +==================+=================================+\n    | -1               | min(sum(abs(x), axis=0))        |\n    +------------------+---------------------------------+\n    | -2               | smallest singular value         |\n    +------------------+---------------------------------+\n    | -inf             | min(sum(abs(x), axis=1))        |\n    +------------------+---------------------------------+\n\n    If ``ord=1``, the norm corresponds to the induced matrix norm where ``p=1`` (i.e., the maximum absolute value column sum).\n\n    If ``ord=2``, the norm corresponds to the induced matrix norm where ``p=inf`` (i.e., the maximum absolute value row sum).\n\n    If ``ord=inf``, the norm corresponds to the induced matrix norm where ``p=2`` (i.e., the largest singular value).\n\n    Default: ``'fro'``.\n\nReturns\n-------\nout: array\n    an array containing the norms for each ``MxN`` matrix. If ``keepdims`` is ``False``, the returned array must have a rank which is two less than the rank of ``x``. If ``x`` has a real-valued data type, the returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`. If ``x`` has a complex-valued data type, the returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type).\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    matrix_power: matrix_power[TArray,]
    "Raises a square matrix (or a stack of square matrices) ``x`` to an integer power ``n``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.\nn: int\n    integer exponent.\n\nReturns\n-------\nout: array\n    if ``n`` is equal to zero, an array containing the identity matrix for each square matrix. If ``n`` is less than zero, an array containing the inverse of each square matrix raised to the absolute value of ``n``, provided that each square matrix is invertible. If ``n`` is greater than zero, an array containing the result of raising each square matrix to the power ``n``. The returned array must have the same shape as ``x`` and a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    matrix_rank: matrix_rank[TArray,]
    "Returns the rank (i.e., number of non-zero singular values) of a matrix (or a stack of matrices).\n\nWhen ``x`` is a stack of matrices, the function must compute the number of non-zero singular values for each matrix in the stack.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a floating-point data type.\nrtol: Optional[Union[float, array]]\n    relative tolerance for small singular values. Singular values approximately less than or equal to ``rtol * largest_singular_value`` are set to zero. If a ``float``, the value is equivalent to a zero-dimensional array having a real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``) and must be broadcast against each matrix. If an ``array``, must have a real-valued floating-point data type and must be compatible with ``shape(x)[:-2]`` (see :ref:`broadcasting`). If ``None``, the default value is ``max(M, N) * eps``, where ``eps`` must be the machine epsilon associated with the real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``). Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing the ranks. The returned array must have the default integer data type and must have shape ``(...)`` (i.e., must have a shape equal to ``shape(x)[:-2]``).\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    matrix_transpose: matrix_transpose[TArray,]
    "Alias for :func:`~array_api.matrix_transpose`."
    outer: outer[TArray,]
    "Returns the outer product of two vectors ``x1`` and ``x2``.\n\nParameters\n----------\nx1: array\n    first one-dimensional input array of size ``N``. Must have a numeric data type.\nx2: array\n    second one-dimensional input array of size ``M``. Must have a numeric data type.\n\nReturns\n-------\nout: array\n    a two-dimensional array containing the outer product and whose shape is ``(N, M)``. The returned array must have a data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    pinv: pinv[TArray,]
    "Returns the (Moore-Penrose) pseudo-inverse of a matrix (or a stack of matrices) ``x``.\n\nThe pseudo-inverse of a matrix :math:`A`, denoted :math:`A^{+}`, is defined as the matrix that \"solves\" the least-squares problem :math:`Ax = b` (i.e., if :math:`\\overline{x}` is a solution, then :math:`A^{+}` is the matrix such that :math:`\\overline{x} = A^{+}b`).\n\nWhile the pseudo-inverse can be defined algebraically, one can understand the pseudo-inverse via singular value decomposition (SVD). Namely, if\n\n.. math::\n   A = U \\Sigma V^H\n\nis a singular decomposition of :math:`A`, then\n\n.. math::\n   A^{+} = U \\Sigma^{+} V^H\n\nwhere :math:`U` and :math:`V^H` are orthogonal matrices, :math:`\\Sigma` is a diagonal matrix consisting of :math:`A`'s singular values, and :math:`\\Sigma^{+}` is then a diagonal matrix consisting of the reciprocals of :math:`A`'s singular values, leaving zeros in place. During numerical computation, only elements larger than a small tolerance are considered nonzero, and all others replaced by zeros.\n\nWhen ``x`` is a stack of matrices, the function must compute the pseudo-inverse for each matrix in the stack.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a floating-point data type.\nrtol: Optional[Union[float, array]]\n    relative tolerance for small singular values. Singular values approximately less than or equal to ``rtol * largest_singular_value`` are set to zero. If a ``float``, the value is equivalent to a zero-dimensional array having a real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``) and must be broadcast against each matrix. If an ``array``, must have a real-valued floating-point data type and must be compatible with ``shape(x)[:-2]`` (see :ref:`broadcasting`). If ``None``, the default value is ``max(M, N) * eps``, where ``eps`` must be the machine epsilon associated with the real-valued floating-point data type determined by :ref:`type-promotion` (as applied to ``x``). Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing the pseudo-inverse(s). The returned array must have a floating-point data type determined by :ref:`type-promotion` and must have shape ``(..., N, M)`` (i.e., must have the same shape as ``x``, except the innermost two dimensions must be transposed).\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    qr: qr[TArray,]
    "Returns the QR decomposition of a full column rank matrix (or a stack of matrices).\n\nIf ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThe **complete QR decomposition** of a matrix :math:`x \\in\\ \\mathbb{K}^{n \\times n}` is defined as\n\n.. math::\n   x = QR\n\nwhere :math:`Q \\in\\ \\mathbb{K}^{m \\times m}` is orthogonal when ``x`` is real-valued and unitary when ``x`` is complex-valued and where :math:`R \\in\\ \\mathbb{K}^{m \\times n}` is an upper triangular matrix with real diagonal (even when ``x`` is complex-valued).\n\nWhen :math:`m \\gt n` (tall matrix), as :math:`R` is upper triangular, the last :math:`m - n` rows are zero. In this case, the last :math:`m - n` columns of :math:`Q` can be dropped to form the **reduced QR decomposition**.\n\n.. math::\n   x = QR\n\nwhere :math:`Q \\in\\ \\mathbb{K}^{m \\times n}` and :math:`R \\in\\ \\mathbb{K}^{n \\times n}`.\n\nThe reduced QR decomposition equals with the complete QR decomposition when :math:`n \\geq m` (wide matrix).\n\nWhen ``x`` is a stack of matrices, the function must compute the QR decomposition for each matrix in the stack.\n\n.. note::\n   Whether an array library explicitly checks whether an input array is a full column rank matrix (or a stack of full column rank matrices) is implementation-defined.\n\n.. warning::\n   The elements in the diagonal of :math:`R` are not necessarily positive. Accordingly, the returned QR decomposition is only unique up to the sign of the diagonal of :math:`R`, and different libraries or inputs on different devices may produce different valid decompositions.\n\n.. warning::\n   The QR decomposition is only well-defined if the first ``k = min(m,n)`` columns of every matrix in ``x`` are linearly independent.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices of rank ``N``. Should have a floating-point data type.\nmode: Literal['reduced', 'complete']\n    decomposition mode. Should be one of the following modes:\n\n    -   ``'reduced'``: compute only the leading ``K`` columns of ``q``, such that ``q`` and ``r`` have dimensions ``(..., M, K)`` and ``(..., K, N)``, respectively, and where ``K = min(M, N)``.\n    -   ``'complete'``: compute ``q`` and ``r`` with dimensions ``(..., M, M)`` and ``(..., M, N)``, respectively.\n\n    Default: ``'reduced'``.\n\nReturns\n-------\nout: Tuple[array, array]\n    a namedtuple ``(Q, R)`` whose\n\n    -   first element must have the field name ``Q`` and must be an array whose shape depends on the value of ``mode`` and contain matrices with orthonormal columns. If ``mode`` is ``'complete'``, the array must have shape ``(..., M, M)``. If ``mode`` is ``'reduced'``, the array must have shape ``(..., M, K)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same size as those of the input array ``x``.\n    -   second element must have the field name ``R`` and must be an array whose shape depends on the value of ``mode`` and contain upper-triangular matrices. If ``mode`` is ``'complete'``, the array must have shape ``(..., M, N)``. If ``mode`` is ``'reduced'``, the array must have shape ``(..., K, N)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same size as those of the input ``x``.\n\n    Each returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    slogdet: slogdet[TArray,]
    "Returns the sign and the natural logarithm of the absolute value of the determinant of a square matrix (or a stack of square matrices) ``x``.\n\n.. note::\n   The purpose of this function is to calculate the determinant more accurately when the determinant is either very small or very large, as calling ``det`` may overflow or underflow.\n\nThe sign of the determinant is given by\n\n.. math::\n   \\operatorname{sign}(\\det x) = \\begin{cases}\n   0 & \\textrm{if } \\det x = 0 \\\\\n   \\frac{\\det x}{|\\det x|} & \\textrm{otherwise}\n   \\end{cases}\n\nwhere :math:`|\\det x|` is the absolute value of the determinant of ``x``.\n\nWhen ``x`` is a stack of matrices, the function must compute the sign and natural logarithm of the absolute value of the determinant for each matrix in the stack.\n\n**Special Cases**\n\nFor real-valued floating-point operands,\n\n- If the determinant is zero, the ``sign`` should be ``0`` and ``logabsdet`` should be ``-infinity``.\n\nFor complex floating-point operands,\n\n- If the determinant is ``0 + 0j``, the ``sign`` should be ``0 + 0j`` and ``logabsdet`` should be ``-infinity + 0j``.\n\n.. note::\n   Depending on the underlying algorithm, when the determinant is zero, the returned result may differ from ``-infinity`` (or ``-infinity + 0j``). In all cases, the determinant should be equal to ``sign * exp(logabsdet)`` (although, again, the result may be subject to numerical precision errors).\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Should have a floating-point data type.\n\nReturns\n-------\nout: Tuple[array, array]\n    a namedtuple (``sign``, ``logabsdet``) whose\n\n    -   first element must have the field name ``sign`` and must be an array containing a number representing the sign of the determinant for each square matrix. Must have the same data type as ``x``.\n    -   second element must have the field name ``logabsdet`` and must be an array containing the natural logarithm of the absolute value of the determinant for each square matrix. If ``x`` is real-valued, the returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`. If ``x`` is complex, the returned array must have a real-valued floating-point data type having the same precision as ``x`` (e.g., if ``x`` is ``complex64``, ``logabsdet`` must have a ``float32`` data type).\n\n    Each returned array must have shape ``shape(x)[:-2]``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    solve: solve[TArray,]
    'Returns the solution of a square system of linear equations with a unique solution.\n\nLet ``x1`` equal :math:`A` and ``x2`` equal :math:`B`. If the promoted data type of ``x1`` and ``x2`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if the promoted data type of ``x1`` and ``x2`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThis function computes the solution :math:`X \\in\\ \\mathbb{K}^{m \\times k}` of the **linear system** associated to :math:`A \\in\\ \\mathbb{K}^{m \\times m}` and :math:`B \\in\\ \\mathbb{K}^{m \\times k}` and is defined as\n\n.. math::\n   AX = B\n\nThis system of linear equations has a unique solution if and only if :math:`A` is invertible.\n\n.. note::\n   Whether an array library explicitly checks whether ``x1`` is invertible is implementation-defined.\n\nWhen ``x1`` and/or ``x2`` is a stack of matrices, the function must compute a solution for each matrix in the stack.\n\nParameters\n----------\nx1: array\n    coefficient array ``A`` having shape ``(..., M, M)`` and whose innermost two dimensions form square matrices. Must be of full rank (i.e., all rows or, equivalently, columns must be linearly independent). Should have a floating-point data type.\nx2: array\n    ordinate (or "dependent variable") array ``B``. If ``x2`` has shape ``(M,)``, ``x2`` is equivalent to an array having shape ``(..., M, 1)``. If ``x2`` has shape ``(..., M, K)``, each column ``k`` defines a set of ordinate values for which to compute a solution, and ``shape(x2)[:-2]`` must be compatible with ``shape(x1)[:-2]`` (see :ref:`broadcasting`). Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array containing the solution to the system ``AX = B`` for each square matrix. If ``x2`` has shape ``(M,)``, the returned array must have shape equal to ``shape(x1)[:-2] + shape(x2)[-1:]``. Otherwise, if ``x2`` has shape ``(..., M, K)```, the returned array must have shape equal to ``(..., M, K)``, where ``...`` refers to the result of broadcasting ``shape(x1)[:-2]`` and ``shape(x2)[:-2]``. The returned array must have a floating-point data type determined by :ref:`type-promotion`.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.'
    svd: svd[TArray,]
    "Returns a singular value decomposition (SVD) of a matrix (or a stack of matrices) ``x``.\n\nIf ``x`` is real-valued, let :math:`\\mathbb{K}` be the set of real numbers :math:`\\mathbb{R}`, and, if ``x`` is complex-valued, let :math:`\\mathbb{K}` be the set of complex numbers :math:`\\mathbb{C}`.\n\nThe full **singular value decomposition** of an :math:`m \\times n` matrix :math:`x \\in\\ \\mathbb{K}^{m \\times n}` is a factorization of the form\n\n.. math::\n   x = U \\Sigma V^H\n\nwhere :math:`U \\in\\ \\mathbb{K}^{m \\times m}`, :math:`\\Sigma \\in\\ \\mathbb{K}^{m \\times\\ n}`, :math:`\\operatorname{diag}(\\Sigma) \\in\\ \\mathbb{R}^{k}` with :math:`k = \\operatorname{min}(m, n)`, :math:`V^H \\in\\ \\mathbb{K}^{n \\times n}`, and where :math:`V^H` is the conjugate transpose when :math:`V` is complex and the transpose when :math:`V` is real-valued. When ``x`` is real-valued, :math:`U`, :math:`V` (and thus :math:`V^H`) are orthogonal, and, when ``x`` is complex, :math:`U`, :math:`V` (and thus :math:`V^H`) are unitary.\n\nWhen :math:`m \\gt n` (tall matrix), we can drop the last :math:`m - n` columns of :math:`U` to form the reduced SVD\n\n.. math::\n   x = U \\Sigma V^H\n\nwhere :math:`U \\in\\ \\mathbb{K}^{m \\times k}`, :math:`\\Sigma \\in\\ \\mathbb{K}^{k \\times\\ k}`, :math:`\\operatorname{diag}(\\Sigma) \\in\\ \\mathbb{R}^{k}`, and :math:`V^H \\in\\ \\mathbb{K}^{k \\times n}`. In this case, :math:`U` and :math:`V` have orthonormal columns.\n\nSimilarly, when :math:`n \\gt m` (wide matrix), we can drop the last :math:`n - m` columns of :math:`V` to also form a reduced SVD.\n\nThis function returns the decomposition :math:`U`, :math:`S`, and :math:`V^H`, where :math:`S = \\operatorname{diag}(\\Sigma)`.\n\nWhen ``x`` is a stack of matrices, the function must compute the singular value decomposition for each matrix in the stack.\n\n.. warning::\n   The returned arrays :math:`U` and :math:`V` are neither unique nor continuous with respect to ``x``. Because :math:`U` and :math:`V` are not unique, different hardware and software may compute different singular vectors.\n\n   Non-uniqueness stems from the fact that multiplying any pair of singular vectors :math:`u_k`, :math:`v_k` by :math:`-1` when ``x`` is real-valued and by :math:`e^{\\phi j}` (:math:`\\phi \\in \\mathbb{R}`) when ``x`` is complex produces another two valid singular vectors of the matrix.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form matrices on which to perform singular value decomposition. Should have a floating-point data type.\nfull_matrices: bool\n    If ``True``, compute full-sized ``U`` and ``Vh``, such that ``U`` has shape ``(..., M, M)`` and ``Vh`` has shape ``(..., N, N)``. If ``False``, compute on the leading ``K`` singular vectors, such that ``U`` has shape ``(..., M, K)`` and ``Vh`` has shape ``(..., K, N)`` and where ``K = min(M, N)``. Default: ``True``.\n\nReturns\n-------\nout: Tuple[array, array, array]\n    a namedtuple ``(U, S, Vh)`` whose\n\n    -   first element must have the field name ``U`` and must be an array whose shape depends on the value of ``full_matrices`` and contain matrices with orthonormal columns (i.e., the columns are left singular vectors). If ``full_matrices`` is ``True``, the array must have shape ``(..., M, M)``. If ``full_matrices`` is ``False``, the array must have shape ``(..., M, K)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. Must have the same data type as ``x``.\n    -   second element must have the field name ``S`` and must be an array with shape ``(..., K)`` that contains the vector(s) of singular values of length ``K``, where ``K = min(M, N)``. For each vector, the singular values must be sorted in descending order by magnitude, such that ``s[..., 0]`` is the largest value, ``s[..., 1]`` is the second largest value, et cetera. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. Must have a real-valued floating-point data type having the same precision as ``x`` (e.g., if ``x`` is ``complex64``, ``S`` must have a ``float32`` data type).\n    -   third element must have the field name ``Vh`` and must be an array whose shape depends on the value of ``full_matrices`` and contain orthonormal rows (i.e., the rows are the right singular vectors and the array is the adjoint). If ``full_matrices`` is ``True``, the array must have shape ``(..., N, N)``. If ``full_matrices`` is ``False``, the array must have shape ``(..., K, N)`` where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. Must have the same data type as ``x``.\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    svdvals: svdvals[TArray,]
    "Returns the singular values of a matrix (or a stack of matrices) ``x``.\n\nWhen ``x`` is a stack of matrices, the function must compute the singular values for each matrix in the stack.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form matrices on which to perform singular value decomposition. Should have a floating-point data type.\n\nReturns\n-------\nout: array\n    an array with shape ``(..., K)`` that contains the vector(s) of singular values of length ``K``, where ``K = min(M, N)``. For each vector, the singular values must be sorted in descending order by magnitude, such that ``s[..., 0]`` is the largest value, ``s[..., 1]`` is the second largest value, et cetera. The first ``x.ndim-2`` dimensions must have the same shape as those of the input ``x``. The returned array must have a real-valued floating-point data type having the same precision as ``x`` (e.g., if ``x`` is ``complex64``, the returned array must have a ``float32`` data type).\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support."
    tensordot: tensordot[TArray,]
    "Alias for :func:`~array_api.tensordot`."
    trace: trace[TArray, TDtype]
    "Returns the sum along the specified diagonals of a matrix (or a stack of matrices) ``x``.\n\nParameters\n----------\nx: array\n    input array having shape ``(..., M, N)`` and whose innermost two dimensions form ``MxN`` matrices. Should have a numeric data type.\noffset: int\n    offset specifying the off-diagonal relative to the main diagonal.\n\n    -   ``offset = 0``: the main diagonal.\n    -   ``offset > 0``: off-diagonal above the main diagonal.\n    -   ``offset < 0``: off-diagonal below the main diagonal.\n\n    Default: ``0``.\ndtype: Optional[dtype]\n    data type of the returned array. If ``None``, the returned array must have the same data type as ``x``, unless ``x`` has an integer data type supporting a smaller range of values than the default integer data type (e.g., ``x`` has an ``int16`` or ``uint32`` data type and the default integer data type is ``int64``). In those latter cases:\n\n    -   if ``x`` has a signed integer data type (e.g., ``int16``), the returned array must have the default integer data type.\n    -   if ``x`` has an unsigned integer data type (e.g., ``uint16``), the returned array must have an unsigned integer data type having the same number of bits as the default integer data type (e.g., if the default integer data type is ``int32``, the returned array must have a ``uint32`` data type).\n\n    If the data type (either specified or resolved) differs from the data type of ``x``, the input array should be cast to the specified data type before computing the sum (rationale: the ``dtype`` keyword argument is intended to help prevent overflows). Default: ``None``.\n\nReturns\n-------\nout: array\n    an array containing the traces and whose shape is determined by removing the last two dimensions and storing the traces in the last array dimension. For example, if ``x`` has rank ``k`` and shape ``(I, J, K, ..., L, M, N)``, then an output array has rank ``k-2`` and shape ``(I, J, K, ..., L)`` where\n\n    ::\n\n      out[i, j, k, ..., l] = trace(a[i, j, k, ..., l, :, :])\n\n    The returned array must have a data type as described by the ``dtype`` parameter above.\n\nNotes\n-----\n\n**Special Cases**\n\nLet ``N`` equal the number of elements over which to compute the sum.\n\n-   If ``N`` is ``0``, the sum is ``0`` (i.e., the empty sum).\n\nFor both real-valued and complex floating-point operands, special cases must be handled as if the operation is implemented by successive application of :func:`~array_api.add`.\n\n.. versionchanged:: 2022.12\n   Added complex data type support.\n\n.. versionchanged:: 2023.12\n   Required the function to return a floating-point array having the same data type as the input array when provided a floating-point array."
    vecdot: vecdot[TArray,]
    "Alias for :func:`~array_api.vecdot`."
    vector_norm: vector_norm[TArray,]
    'Computes the vector norm of a vector (or batch of vectors) ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\naxis: Optional[Union[int, Tuple[int, ...]]]\n    If an integer, ``axis`` specifies the axis (dimension) along which to compute vector norms. If an n-tuple, ``axis`` specifies the axes (dimensions) along which to compute batched vector norms. If ``None``, the vector norm must be computed over all array values (i.e., equivalent to computing the vector norm of a flattened array). Negative indices must be supported. Default: ``None``.\nkeepdims: bool\n    If ``True``, the axes (dimensions) specified by ``axis`` must be included in the result as singleton dimensions, and, accordingly, the result must be compatible with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the axes (dimensions) specified by ``axis`` must not be included in the result. Default: ``False``.\nord: Union[int, float, Literal[inf, -inf]]\n    order of the norm. The following mathematical norms must be supported:\n\n    +------------------+----------------------------+\n    | ord              | description                |\n    +==================+============================+\n    | 1                | L1-norm (Manhattan)        |\n    +------------------+----------------------------+\n    | 2                | L2-norm (Euclidean)        |\n    +------------------+----------------------------+\n    | inf              | infinity norm              |\n    +------------------+----------------------------+\n    | (int,float >= 1) | p-norm                     |\n    +------------------+----------------------------+\n\n    The following non-mathematical "norms" must be supported:\n\n    +------------------+--------------------------------+\n    | ord              | description                    |\n    +==================+================================+\n    | 0                | sum(a != 0)                    |\n    +------------------+--------------------------------+\n    | -1               | 1./sum(1./abs(a))              |\n    +------------------+--------------------------------+\n    | -2               | 1./sqrt(sum(1./abs(a)\\*\\*2))   |\n    +------------------+--------------------------------+\n    | -inf             | min(abs(a))                    |\n    +------------------+--------------------------------+\n    | (int,float < 1)  | sum(abs(a)\\*\\*ord)\\*\\*(1./ord) |\n    +------------------+--------------------------------+\n\n    Default: ``2``.\n\nReturns\n-------\nout: array\n    an array containing the vector norms. If ``axis`` is ``None``, the returned array must be a zero-dimensional array containing a vector norm. If ``axis`` is a scalar value (``int`` or ``float``), the returned array must have a rank which is one less than the rank of ``x``. If ``axis`` is a ``n``-tuple, the returned array must have a rank which is ``n`` less than the rank of ``x``. If ``x`` has a real-valued data type, the returned array must have a real-valued floating-point data type determined by :ref:`type-promotion`. If ``x`` has a complex-valued data type, the returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type).\n\nNotes\n-----\n\n.. versionchanged:: 2022.12\n   Added complex data type support.'


@runtime_checkable
class FftNamespace[TArray: Array, TDevice](Protocol):
    fft: fft[TArray,]
    "Computes the one-dimensional discrete Fourier transform.\n\n.. note::\n   Applying the one-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifft(fft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (number of elements, axis, and normalization mode).\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\nn: Optional[int]\n    number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.\n\n    -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.\n    -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.\n    -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.\n\n    Default: ``None``.\naxis: int\n    axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: no normalization.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: normalize by ``1/n``.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axis (dimension) specified by ``axis``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array."
    ifft: ifft[TArray,]
    "Computes the one-dimensional inverse discrete Fourier transform.\n\n.. note::\n   Applying the one-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifft(fft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (number of elements, axis, and normalization mode).\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\nn: Optional[int]\n    number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.\n\n    -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.\n    -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.\n    -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.\n\n    Default: ``None``.\naxis: int\n    axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: normalize by ``1/n``.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: no normalization.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axis (dimension) specified by ``axis``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array."
    fftn: fftn[TArray,]
    "Computes the n-dimensional discrete Fourier transform.\n\n.. note::\n   Applying the n-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifftn(fftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (sizes, axes, and normalization mode).\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\ns: Optional[Sequence[int]]\n    number of elements over which to compute the transform along the axes (dimensions) specified by ``axes``. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``.\n\n    -   If ``s[i]`` is greater than ``M[i]``, axis ``i`` must be zero-padded to size ``s[i]``.\n    -   If ``s[i]`` is less than ``M[i]``, axis ``i`` must be trimmed to size ``s[i]``.\n    -   If ``s[i]`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` must be used when computing the transform.\n\n    If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.\naxes: Optional[Sequence[int]]\n    axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).\n\n    If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.\n\n    If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: no normalization.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: normalize by ``1/n``.\n\n    where ``n = prod(s)`` is the logical FFT size.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axes (dimensions) specified by ``axes``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axes specified by ``axes`` which must have size ``s[i]``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array."
    ifftn: ifftn[TArray,]
    "Computes the n-dimensional inverse discrete Fourier transform.\n\n.. note::\n   Applying the n-dimensional inverse discrete Fourier transform to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``ifftn(fftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (sizes, axes, and normalization mode).\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\ns: Optional[Sequence[int]]\n    number of elements over which to compute the transform along the axes (dimensions) specified by ``axes``. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``.\n\n    -   If ``s[i]`` is greater than ``M[i]``, axis ``i`` must be zero-padded to size ``s[i]``.\n    -   If ``s[i]`` is less than ``M[i]``, axis ``i`` must be trimmed to size ``s[i]``.\n    -   If ``s[i]`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` must be used when computing the transform.\n\n    If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.\naxes: Optional[Sequence[int]]\n    axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).\n\n    If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.\n\n    If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.\nnorm: Literal['backward', 'ortho', 'forward']\n    specify the normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: normalize by ``1/n``.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: no normalization.\n\n    where ``n = prod(s)`` is the logical FFT size.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axes (dimensions) specified by ``axes``. The returned array must have the same data type as ``x`` and must have the same shape as ``x``, except for the axes specified by ``axes`` which must have size ``s[i]``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the input array have a complex floating-point data type and required that the output array have the same data type as the input array."
    rfft: rfft[TArray,]
    "Computes the one-dimensional discrete Fourier transform for real-valued input.\n\n.. note::\n   Applying the one-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfft(rfft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axis and normalization mode) and consistent values for the number of elements over which to compute the transforms.\n\nParameters\n----------\nx: array\n    input array. Must have a real-valued floating-point data type.\nn: Optional[int]\n    number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.\n\n    -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.\n    -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.\n    -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.\n\n    Default: ``None``.\naxis: int\n    axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: no normalization.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: normalize by ``1/n``.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a complex floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``float64``, then the returned array must have a ``complex128`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n//2 + 1``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    irfft: irfft[TArray,]
    "Computes the one-dimensional inverse of ``rfft`` for complex-valued input.\n\n.. note::\n   Applying the one-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfft(rfft(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axis and normalization mode) and consistent values for the number of elements over which to compute the transforms.\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\nn: Optional[int]\n    number of elements along the transformed axis (dimension) specified by ``axis`` in the **output array**. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``2*(M-1)``.\n\n    -   If ``n//2+1`` is greater than ``M``, the axis of the input array specified by ``axis`` must be zero-padded to size ``n//2+1``.\n    -   If ``n//2+1`` is less than ``M``, the axis of the input array specified by ``axis`` must be trimmed to size ``n//2+1``.\n    -   If ``n//2+1`` equals ``M``, all elements along the axis of the input array specified by ``axis`` must be used when computing the transform.\n\n    Default: ``None``.\naxis: int\n    axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: normalize by ``1/n``.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: no normalization.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.\n\nNotes\n-----\n\n-   In order to return an array having an odd number of elements along the transformed axis, the function must be provided an odd integer for ``n``.\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the output array have a real-valued floating-point data type having the same precision as the input array."
    rfftn: rfftn[TArray,]
    "Computes the n-dimensional discrete Fourier transform for real-valued input.\n\n.. note::\n   Applying the n-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfftn(rfftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axes and normalization mode) and consistent sizes.\n\nParameters\n----------\nx: array\n    input array. Must have a real-valued floating-point data type.\ns: Optional[Sequence[int]]\n    number of elements over which to compute the transform along axes (dimensions) specified by ``axes``. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``.\n\n    -   If ``s[i]`` is greater than ``M[i]``, axis ``i`` must be zero-padded to size ``s[i]``.\n    -   If ``s[i]`` is less than ``M[i]``, axis ``i`` must be trimmed to size ``s[i]``.\n    -   If ``s[i]`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` must be used when computing the transform.\n\n    If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.\naxes: Optional[Sequence[int]]\n    axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).\n\n    If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.\n\n    If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: no normalization.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: normalize by ``1/n``.\n\n    where ``n = prod(s)``, the logical FFT size.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axes (dimension) specified by ``axes``. The returned array must have a complex floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``float64``, then the returned array must have a ``complex128`` data type). The returned array must have the same shape as ``x``, except for the last transformed axis which must have size ``s[-1]//2 + 1`` and the remaining transformed axes which must have size ``s[i]``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    irfftn: irfftn[TArray,]
    "Computes the n-dimensional inverse of ``rfftn`` for complex-valued input.\n\n.. note::\n   Applying the n-dimensional inverse discrete Fourier transform for real-valued input to the output of this function must return the original (i.e., non-transformed) input array within numerical accuracy (i.e., ``irfftn(rfftn(x)) == x``), provided that the transform and inverse transform are performed with the same arguments (axes and normalization mode) and consistent sizes.\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\ns: Optional[Sequence[int]]\n    number of elements along the transformed axes (dimensions) specified by ``axes`` in the **output array**. Let ``i`` be the index of the ``n``-th axis specified by ``axes`` (i.e., ``i = axes[n]``) and ``M[i]`` be the size of the input array along axis ``i``. When ``s`` is ``None``, the function must set ``s`` equal to a sequence of integers such that ``s[i]`` equals ``M[i]`` for all ``i``, except for the last transformed axis in which ``s[i]`` equals ``2*(M[i]-1)``. For each ``i``, let ``n`` equal ``s[i]``, except for the last transformed axis in which ``n`` equals ``s[i]//2+1``.\n\n    -   If ``n`` is greater than ``M[i]``, axis ``i`` of the input array must be zero-padded to size ``n``.\n    -   If ``n`` is less than ``M[i]``, axis ``i`` of the input array must be trimmed to size ``n``.\n    -   If ``n`` equals ``M[i]`` or ``-1``, all elements along axis ``i`` of the input array must be used when computing the transform.\n\n    If ``s`` is not ``None``, ``axes`` must not be ``None``. Default: ``None``.\naxes: Optional[Sequence[int]]\n    axes (dimensions) over which to compute the transform. A valid axis in ``axes`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an axis is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension).\n\n    If ``s`` is provided, the corresponding ``axes`` to be transformed must also be provided. If ``axes`` is ``None``, the function must compute the transform over all axes. Default: ``None``.\n\n    If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: normalize by ``1/n``.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: no normalization.\n\n    where ``n = prod(s)`` is the logical FFT size.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axes (dimension) specified by ``axes``. The returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type). The returned array must have the same shape as ``x``, except for the transformed axes which must have size ``s[i]``.\n\nNotes\n-----\n\n-   In order to return an array having an odd number of elements along the last transformed axis, the function must be provided an odd integer for ``s[-1]``.\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the output array have a real-valued floating-point data type having the same precision as the input array."
    hfft: hfft[TArray,]
    "Computes the one-dimensional discrete Fourier transform of a signal with Hermitian symmetry.\n\nParameters\n----------\nx: array\n    input array. Should have a complex floating-point data type.\nn: Optional[int]\n    number of elements along the transformed axis (dimension) specified by ``axis`` in the **output array**. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``2*(M-1)``.\n\n    -   If ``n//2+1`` is greater than ``M``, the axis of the input array specified by ``axis`` must be zero-padded to length ``n//2+1``.\n    -   If ``n//2+1`` is less than ``M``, the axis of the input array specified by ``axis`` must be trimmed to size ``n//2+1``.\n    -   If ``n//2+1`` equals ``M``, all elements along the axis of the input array specified by ``axis`` must be used when computing the transform.\n\n    Default: ``None``.\naxis: int\n    axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: no normalization.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: normalize by ``1/n``.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a real-valued floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``complex128``, then the returned array must have a ``float64`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the input array to have a complex floating-point data type and required that the output array have a real-valued data type having the same precision as the input array."
    ihfft: ihfft[TArray,]
    "Computes the one-dimensional inverse discrete Fourier transform of a signal with Hermitian symmetry.\n\nParameters\n----------\nx: array\n    input array. Must have a real-valued floating-point data type.\nn: Optional[int]\n    number of elements over which to compute the transform along the axis (dimension) specified by ``axis``. Let ``M`` be the size of the input array along the axis specified by ``axis``. When ``n`` is ``None``, the function must set ``n`` equal to ``M``.\n\n    -   If ``n`` is greater than ``M``, the axis specified by ``axis`` must be zero-padded to size ``n``.\n    -   If ``n`` is less than ``M``, the axis specified by ``axis`` must be trimmed to size ``n``.\n    -   If ``n`` equals ``M``, all elements along the axis specified by ``axis`` must be used when computing the transform.\n\n    Default: ``None``.\naxis: int\n    axis (dimension) of the input array over which to compute the transform. A valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank (number of dimensions) of ``x``. If an ``axis`` is specified as a negative integer, the function must determine the axis along which to compute the transform by counting backward from the last dimension (where ``-1`` refers to the last dimension). Default: ``-1``.\nnorm: Literal['backward', 'ortho', 'forward']\n    normalization mode. Should be one of the following modes:\n\n    - ``'backward'``: normalize by ``1/n``.\n    - ``'ortho'``: normalize by ``1/sqrt(n)`` (i.e., make the FFT orthonormal).\n    - ``'forward'``: no normalization.\n\n    Default: ``'backward'``.\n\nReturns\n-------\nout: array\n    an array transformed along the axis (dimension) specified by ``axis``. The returned array must have a complex floating-point data type whose precision matches the precision of ``x`` (e.g., if ``x`` is ``float64``, then the returned array must have a ``complex128`` data type). The returned array must have the same shape as ``x``, except for the axis specified by ``axis`` which must have size ``n//2 + 1``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    fftfreq: fftfreq[TArray, TDevice]
    "Computes the discrete Fourier transform sample frequencies.\n\nFor a Fourier transform of length ``n`` and length unit of ``d``, the frequencies are described as:\n\n.. code-block::\n\n  f = [0, 1, ..., n/2-1, -n/2, ..., -1] / (d*n)        # if n is even\n  f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)  # if n is odd\n\nParameters\n----------\nn: int\n    window length.\nd: float\n    sample spacing between individual samples of the Fourier transform input. Default: ``1.0``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array of shape ``(n,)`` containing the sample frequencies. The returned array must have the default real-valued floating-point data type.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the output array have the default real-valued floating-point data type."
    rfftfreq: rfftfreq[TArray, TDevice]
    "Computes the discrete Fourier transform sample frequencies (for ``rfft`` and ``irfft``).\n\nFor a Fourier transform of length ``n`` and length unit of ``d``, the frequencies are described as:\n\n.. code-block::\n\n  f = [0, 1, ...,     n/2-1,     n/2] / (d*n)  # if n is even\n  f = [0, 1, ..., (n-1)/2-1, (n-1)/2] / (d*n)  # if n is odd\n\nThe Nyquist frequency component is considered to be positive.\n\nParameters\n----------\nn: int\n    window length.\nd: float\n    sample spacing between individual samples of the Fourier transform input. Default: ``1.0``.\ndevice: Optional[device]\n    device on which to place the created array. Default: ``None``.\n\nReturns\n-------\nout: array\n    an array of shape ``(n//2+1,)`` containing the sample frequencies. The returned array must have the default real-valued floating-point data type.\n\nNotes\n-----\n\n.. versionadded:: 2022.12\n\n.. versionchanged:: 2023.12\n   Required the output array have the default real-valued floating-point data type."
    fftshift: fftshift[TArray,]
    "Shifts the zero-frequency component to the center of the spectrum.\n\nThis function swaps half-spaces for all axes (dimensions) specified by ``axes``.\n\n.. note::\n   ``out[0]`` is the Nyquist component only if the length of the input is even.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\naxes: Optional[Union[int, Sequence[int]]]\n    axes over which to shift. If ``None``, the function must shift all axes. Default: ``None``.\n\n    If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.\n\nReturns\n-------\nout: array\n    the shifted array. The returned array must have the same data type and shape as ``x``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"
    ifftshift: ifftshift[TArray,]
    "Inverse of ``fftshift``.\n\n.. note::\n   Although identical for even-length ``x``, ``fftshift`` and ``ifftshift`` differ by one sample for odd-length ``x``.\n\nParameters\n----------\nx: array\n    input array. Should have a floating-point data type.\naxes: Optional[Union[int, Sequence[int]]]\n    axes over which to perform the inverse shift. If ``None``, the function must shift all axes. Default: ``None``.\n\n    If ``axes`` contains two or more entries which resolve to the same axis (i.e., resolved axes are not unique), the behavior is unspecified and thus implementation-defined.\n\nReturns\n-------\nout: array\n    the shifted array. The returned array must have the same data type and shape as ``x``.\n\nNotes\n-----\n\n.. versionadded:: 2022.12"


@runtime_checkable
class ArrayNamespaceFull[TArray: Array, TDtype, TDevice](ArrayNamespace[TArray, TDtype, TDevice], Protocol):
    linalg: LinalgNamespace[TArray, TDtype]
    fft: FftNamespace[TArray, TDevice]


@runtime_checkable
class ShapedArray[*T, TDevice, TDtype](Array[TDevice, TDtype], Protocol):
    @property
    def shape(self) -> tuple[*T]: ...  # type: ignore[override]


type ShapedAnyArray[*T] = ShapedArray[*T, Any, Any]
