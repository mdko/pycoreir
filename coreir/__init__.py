from ctypes import cdll
import ctypes as ct
import platform
import os
from coreir.lib import load_shared_lib, libcoreir_c
from coreir.context import COREContext, COREContext_p, Context, COREMapKind, COREMapKind_STR2PARAM_MAP, BitVector
from coreir.module import Module, COREModule, COREModule_p, COREModuleDef, COREModuleDef_p, ModuleDef, Module, \
        COREDirectedInstance_p, COREDirectedConnection_p, COREDirectedModule_p
from coreir.generator import COREGenerator, COREGenerator_p, Generator
from coreir.namespace import CORENamespace, CORENamespace_p
from coreir.type import COREType, COREType_p, CoreIRType, Params, Value, Values, COREValue, COREValue_p, Type, NamedType, COREValueType_p
from coreir.wireable import COREWireable_p, Wireable
from coreir.type_gen import type_gen
from coreir.simulator import SimulatorState, CORESimulatorState_p, CORESimValue_p
from collections import namedtuple

class COREConnection(ct.Structure):
    pass

COREConnection_p = ct.POINTER(COREConnection)

libcoreir_c.CORENewMap.argtypes = [COREContext_p, ct.c_void_p, ct.c_void_p, ct.c_uint32, COREMapKind]
libcoreir_c.CORENewMap.restype = ct.c_void_p

libcoreir_c.CORENewContext.restype = COREContext_p

libcoreir_c.COREContextNamed.argtypes = [COREContext_p, ct.c_char_p, ct.c_char_p]
libcoreir_c.COREContextNamed.restype = COREType_p

libcoreir_c.COREContextBool.argstypes = [COREContext_p]
libcoreir_c.COREContextBool.restype = COREType_p

libcoreir_c.COREContextInt.argstypes = [COREContext_p]
libcoreir_c.COREContextInt.restype = COREType_p

libcoreir_c.COREContextBitVector.argstypes = [COREContext_p]
libcoreir_c.COREContextBitVector.restype = COREType_p

libcoreir_c.COREContextString.argstypes = [COREContext_p]
libcoreir_c.COREContextString.restype = COREType_p

libcoreir_c.COREContextCoreIRType.argstypes = [COREContext_p]
libcoreir_c.COREContextCoreIRType.restype = COREType_p

libcoreir_c.COREContextRunPasses.argstypes = [COREContext_p, ct.POINTER(ct.c_char_p), ct.c_int]
libcoreir_c.COREContextRunPasses.restype = ct.c_bool

libcoreir_c.COREPrintErrors.argtypes = [COREContext_p]

libcoreir_c.COREBitIn.argtypes = [COREContext_p]
libcoreir_c.COREBitIn.restype = COREType_p

libcoreir_c.COREBit.argtypes = [COREContext_p]
libcoreir_c.COREBit.restype = COREType_p

libcoreir_c.COREArray.argtypes = [COREContext_p, ct.c_uint32, COREType_p]
libcoreir_c.COREArray.restype = COREType_p

libcoreir_c.CORERecord.argtypes = [COREContext_p, ct.c_void_p]
libcoreir_c.CORERecord.restype = COREType_p

libcoreir_c.COREPrintType.argtypes = [COREType_p, ]

libcoreir_c.CORELoadModule.argtypes = [COREContext_p, ct.c_char_p, ct.POINTER(ct.c_bool)]
libcoreir_c.CORELoadModule.restype = COREModule_p

libcoreir_c.CORESaveModule.argtypes = [COREModule_p, ct.c_char_p, ct.POINTER(ct.c_bool)]

libcoreir_c.COREGetGlobal.argtypes = [COREContext_p]
libcoreir_c.COREGetGlobal.restype = CORENamespace_p

libcoreir_c.COREGetNamespace.argtypes = [COREContext_p, ct.c_char_p]
libcoreir_c.COREGetNamespace.restype = CORENamespace_p

libcoreir_c.CORENewModule.argtypes = [CORENamespace_p, ct.c_char_p, COREType_p, ct.c_void_p]
libcoreir_c.CORENewModule.restype = COREModule_p

libcoreir_c.COREModuleHasDef.argtypes = [COREModule_p]
libcoreir_c.COREModuleHasDef.restype = ct.c_bool

libcoreir_c.COREModuleSetDef.argtypes = [COREModule_p, COREModuleDef_p]

libcoreir_c.COREPrintModule.argtypes = [COREModule_p]

libcoreir_c.COREModuleNewDef.argtypes = [COREModule_p]
libcoreir_c.COREModuleNewDef.restype = COREModuleDef_p

libcoreir_c.COREModuleGetName.argtypes = [COREModule_p]
libcoreir_c.COREModuleGetName.restype = ct.c_char_p

libcoreir_c.COREModuleGetType.argtypes = [COREModule_p]
libcoreir_c.COREModuleGetType.restype = COREType_p

libcoreir_c.COREGeneratorGetName.argtypes = [COREGenerator_p]
libcoreir_c.COREGeneratorGetName.restype = ct.c_char_p

libcoreir_c.COREModuleGetDef.argtypes = [COREModule_p]
libcoreir_c.COREModuleGetDef.restype = COREModuleDef_p

libcoreir_c.COREModuleDefAddModuleInstance.argtypes = [COREModuleDef_p, ct.c_char_p, COREModule_p, ct.c_void_p]
libcoreir_c.COREModuleDefAddModuleInstance.restype = COREWireable_p

libcoreir_c.COREModuleDefAddGeneratorInstance.argtypes = [COREModuleDef_p, ct.c_char_p, COREGenerator_p, ct.c_void_p, ct.c_void_p]
libcoreir_c.COREModuleDefAddGeneratorInstance.restype = COREWireable_p

libcoreir_c.COREModuleDefGetInterface.argtypes = [COREModuleDef_p]
libcoreir_c.COREModuleDefGetInterface.restype = COREWireable_p

libcoreir_c.COREModuleDefInstancesIterBegin.argtypes = [COREModuleDef_p]
libcoreir_c.COREModuleDefInstancesIterBegin.restype = COREWireable_p

libcoreir_c.COREModuleDefInstancesIterEnd.argtypes = [COREModuleDef_p]
libcoreir_c.COREModuleDefInstancesIterEnd.restype = COREWireable_p

libcoreir_c.COREModuleDefInstancesIterNext.argtypes = [COREModuleDef_p, COREWireable_p]
libcoreir_c.COREModuleDefInstancesIterNext.restype = COREWireable_p

libcoreir_c.COREModuleGetDirectedModule.argtypes = [COREModule_p]
libcoreir_c.COREModuleGetDirectedModule.restype = COREDirectedModule_p

libcoreir_c.COREGetModuleRef.argtypes = [COREWireable_p]
libcoreir_c.COREGetModuleRef.restype = COREModule_p

libcoreir_c.COREGetModArg.argtypes = [COREWireable_p, ct.c_char_p]
libcoreir_c.COREGetModArg.restype = COREValue_p

libcoreir_c.COREHasModArg.argtypes = [COREWireable_p, ct.c_char_p]
libcoreir_c.COREHasModArg.restype = ct.c_bool

libcoreir_c.COREGetValueType.argtypes = [COREValue_p]
libcoreir_c.COREGetValueType.restype = ct.c_int

libcoreir_c.COREValueStringGet.argtypes = [COREValue_p]
libcoreir_c.COREValueStringGet.restype = ct.c_char_p

libcoreir_c.COREValueIntGet.argtypes = [COREValue_p]
libcoreir_c.COREValueIntGet.restype = ct.c_int

libcoreir_c.COREValueBoolGet.argtypes = [COREValue_p]
libcoreir_c.COREValueBoolGet.restype = ct.c_bool

libcoreir_c.COREValueBitVectorGet.argtypes = [COREValue_p, ct.POINTER(ct.c_int), ct.POINTER(ct.c_uint64)]
libcoreir_c.COREValueBitVectorGet.restype = None

libcoreir_c.COREValueInt.argtypes = [COREContext_p, ct.c_int]
libcoreir_c.COREValueInt.restype = COREValue_p

libcoreir_c.COREValueString.argtypes = [COREContext_p, ct.c_char_p]
libcoreir_c.COREValueString.restype = COREValue_p

libcoreir_c.COREValueBool.argtypes = [COREContext_p, ct.c_bool]
libcoreir_c.COREValueBool.restype = COREValue_p

libcoreir_c.COREValueBitVector.argtypes = [COREContext_p, ct.c_int, ct.c_uint64]
libcoreir_c.COREValueBitVector.restype = COREValue_p

libcoreir_c.COREModuleDefGetConnections.argtypes = [COREModuleDef_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREModuleDefGetConnections.restype = ct.POINTER(COREConnection_p)

libcoreir_c.COREConnectionGetFirst.argtypes = [COREConnection_p]
libcoreir_c.COREConnectionGetFirst.restype = COREWireable_p

libcoreir_c.COREConnectionGetSecond.argtypes = [COREConnection_p]
libcoreir_c.COREConnectionGetSecond.restype = COREWireable_p

libcoreir_c.COREModuleDefConnect.argtypes = [COREModuleDef_p, COREWireable_p, COREWireable_p]

libcoreir_c.COREPrintModuleDef.argtypes = [COREModuleDef_p]

libcoreir_c.COREWireableGetConnectedWireables.argtypes = [COREWireable_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREWireableGetConnectedWireables.restype = ct.POINTER(COREWireable_p)

libcoreir_c.COREWireableGetModuleDef.argtypes = [COREWireable_p]
libcoreir_c.COREWireableGetModuleDef.restype = COREModuleDef_p

libcoreir_c.COREWireableSelect.argtypes = [COREWireable_p, ct.c_char_p]
libcoreir_c.COREWireableSelect.restype = COREWireable_p

libcoreir_c.COREWireableCanSelect.argtypes = [COREWireable_p, ct.c_char_p]
libcoreir_c.COREWireableCanSelect.restype = ct.c_bool

libcoreir_c.COREWireableGetSelectPath.argtypes = [COREWireable_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREWireableGetSelectPath.restype = ct.POINTER(ct.c_char_p)

libcoreir_c.COREWireableGetType.argtypes = [COREWireable_p]
libcoreir_c.COREWireableGetType.restype = COREType_p

libcoreir_c.COREModuleDefSelect.argtypes = [COREModuleDef_p, ct.c_char_p]
libcoreir_c.COREModuleDefSelect.restype = COREWireable_p

libcoreir_c.COREModuleDefGetModule.argtypes = [COREModuleDef_p]
libcoreir_c.COREModuleDefGetModule.restype = COREModule_p

libcoreir_c.CORENamespaceGetName.argtypes = [CORENamespace_p]
libcoreir_c.CORENamespaceGetName.restype = ct.c_char_p

# libcoreir_c.CORESelectGetParent.argtypes = [COREWireable_p]
# libcoreir_c.CORESelectGetParent.restype = COREWireable_p

libcoreir_c.COREDirectedModuleSel.argtypes = [COREDirectedModule_p, ct.POINTER(ct.c_char_p), ct.c_int]
libcoreir_c.COREDirectedModuleSel.restype = COREWireable_p

libcoreir_c.COREDirectedModuleGetInstances.argtypes = [COREDirectedModule_p, ct.POINTER(ct.c_uint)]
libcoreir_c.COREDirectedModuleGetInstances.restype = ct.POINTER(COREDirectedInstance_p)

libcoreir_c.COREDirectedModuleGetInputs.argtypes = [COREDirectedModule_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedModuleGetInputs.restype = ct.POINTER(COREDirectedConnection_p)

libcoreir_c.COREDirectedModuleGetOutputs.argtypes = [COREDirectedModule_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedModuleGetOutputs.restype = ct.POINTER(COREDirectedConnection_p)

libcoreir_c.COREDirectedModuleGetConnections.argtypes = [COREDirectedModule_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedModuleGetConnections.restype = ct.POINTER(COREDirectedConnection_p)

libcoreir_c.COREDirectedConnectionGetSrc.argtypes = [COREDirectedConnection_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedConnectionGetSrc.restype = ct.POINTER(ct.c_char_p)

libcoreir_c.COREDirectedConnectionGetSnk.argtypes = [COREDirectedConnection_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedConnectionGetSnk.restype = ct.POINTER(ct.c_char_p)

libcoreir_c.COREDirectedInstanceGetInputs.argtypes = [COREDirectedInstance_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedInstanceGetInputs.restype = ct.POINTER(COREDirectedConnection_p)

libcoreir_c.COREDirectedInstanceGetOutputs.argtypes = [COREDirectedInstance_p, ct.POINTER(ct.c_int)]
libcoreir_c.COREDirectedInstanceGetOutputs.restype = ct.POINTER(COREDirectedConnection_p)

libcoreir_c.COREArrayTypeGetLen.argtypes = [COREType_p]
libcoreir_c.COREArrayTypeGetLen.restype = ct.c_uint

libcoreir_c.COREGetTypeKind.argtypes = [COREType_p]
libcoreir_c.COREGetTypeKind.restype = ct.c_int # CORETypeKind is an enum

libcoreir_c.CORETypeGetSize.argtypes = [COREType_p]
libcoreir_c.CORETypeGetSize.restype = ct.c_uint

libcoreir_c.COREModuleGetGenArgs.argtypes = [COREModule_p, ct.POINTER(ct.POINTER(ct.c_char_p)), ct.POINTER(ct.POINTER(COREValue_p)), ct.POINTER(ct.c_int)]
libcoreir_c.COREModuleGetGenArgs.restype = None

libcoreir_c.COREModuleIsGenerated.argtypes = [COREModule_p]
libcoreir_c.COREModuleIsGenerated.restype = ct.c_bool

libcoreir_c.CORENamespaceGetGenerator.argtypes = [CORENamespace_p, ct.c_char_p]
libcoreir_c.CORENamespaceGetGenerator.restype = COREGenerator_p

libcoreir_c.CORENamespaceHasGenerator.argtypes = [CORENamespace_p, ct.c_char_p]
libcoreir_c.CORENamespaceHasGenerator.restype = ct.c_bool

libcoreir_c.CORENamespaceGetModule.argtypes = [CORENamespace_p, ct.c_char_p]
libcoreir_c.CORENamespaceGetModule.restype = COREModule_p

libcoreir_c.CORENamespaceHasModule.argtypes = [CORENamespace_p, ct.c_char_p]
libcoreir_c.CORENamespaceHasModule.restype = ct.c_bool

libcoreir_c.COREGeneratorGetName.argtypes = [COREGenerator_p]
libcoreir_c.COREGeneratorGetName.restype = ct.c_char_p

libcoreir_c.COREGeneratorGetGenParams.argtypes = [COREGenerator_p, ct.POINTER(ct.POINTER(ct.c_char_p)), ct.POINTER(ct.POINTER(COREValueType_p)), ct.POINTER(ct.c_int)]
libcoreir_c.COREGeneratorGetGenParams.restype = None

libcoreir_c.CORERecordTypeGetItems.argtypes = [COREType_p, ct.POINTER(ct.POINTER(ct.c_char_p)), ct.POINTER(ct.POINTER(COREType_p)), ct.POINTER(ct.c_int)]

libcoreir_c.CORENamedTypeToString.argtypes = [COREType_p]
libcoreir_c.CORENamedTypeToString.restype = ct.c_char_p

libcoreir_c.CORESimValueGetBit.argtypes = [CORESimValue_p, ct.c_int]
libcoreir_c.CORESimValueGetBit.restype = ct.c_bool

libcoreir_c.CORESimValueGetLength.argtypes = [CORESimValue_p]
libcoreir_c.CORESimValueGetLength.restype = ct.c_int

libcoreir_c.CORENewSimulatorState.argtypes = [COREModule_p]
libcoreir_c.CORENewSimulatorState.restype = CORESimulatorState_p

libcoreir_c.COREDeleteSimulatorState.argtypes = [CORESimulatorState_p]
libcoreir_c.COREDeleteSimulatorState.restype = None

libcoreir_c.CORESimGetValueByOriginalName.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int, ct.POINTER(ct.c_char_p), ct.c_int]
libcoreir_c.CORESimGetValueByOriginalName.restype = CORESimValue_p

libcoreir_c.CORESimResetCircuit.argtypes = [CORESimulatorState_p]
libcoreir_c.CORESimResetCircuit.restype = None

libcoreir_c.CORESimRunHalfCycle.argtypes = [CORESimulatorState_p]
libcoreir_c.CORESimRunHalfCycle.restype = None

libcoreir_c.CORESimSetClock.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int, ct.c_bool, ct.c_bool]
libcoreir_c.CORESimSetClock.restype = None

libcoreir_c.CORESimSetMainClock.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int]
libcoreir_c.CORESimSetMainClock.restype = None

libcoreir_c.CORESimGetClockCycles.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int]
libcoreir_c.CORESimGetClockCycles.restype = ct.c_int

libcoreir_c.CORESimSetValue.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int, ct.POINTER(ct.c_bool), ct.c_int]
libcoreir_c.CORESimSetValue.restype = None

libcoreir_c.CORESimStepMainClock.argtypes = [CORESimulatorState_p]
libcoreir_c.CORESimStepMainClock.restype = None

libcoreir_c.CORESimRun.argtypes = [CORESimulatorState_p]
libcoreir_c.CORESimRun.restype = None

libcoreir_c.CORESimExecute.argtypes = [CORESimulatorState_p]
libcoreir_c.CORESimExecute.restype = None

libcoreir_c.CORESimRewind.argtypes = [CORESimulatorState_p, ct.c_int]
libcoreir_c.CORESimRewind.restype = ct.c_bool

libcoreir_c.CORESimSetWatchPointByOriginalName.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int, ct.POINTER(ct.c_char_p), ct.c_int, ct.POINTER(ct.c_bool), ct.c_int]
libcoreir_c.CORESimSetWatchPointByOriginalName.restype = None

libcoreir_c.CORESimSetWatchPointByOriginalName.argtypes = [CORESimulatorState_p, ct.POINTER(ct.c_char_p), ct.c_int, ct.POINTER(ct.c_char_p), ct.c_int]
libcoreir_c.CORESimSetWatchPointByOriginalName.restype = None

libcoreir_c.COREInstanceGetInstname.argtypes = [COREWireable_p]
libcoreir_c.COREInstanceGetInstname.restype = ct.c_char_p

libcoreir_c.CORETypeIsInput.argtypes = [COREType_p]
libcoreir_c.CORETypeIsInput.restype = ct.c_bool
