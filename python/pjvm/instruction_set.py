#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PC的计算依然需要确认


def nop(code, pc):
    return pc


def bipush(code, pc):  # DONE
    # 补码处理
    short = code[pc]
    pc += 1

    if short >= 128:
        short -= 256
        # 之前的傻X方法
        # tab = string.maketrans("01", "10")
        # short = -(int(bin(short)[2:].translate(tab), 2) + 1)
    vm_stack.push(short)
    return pc


def sipush(code, pc):  # DONE
    short1 = code[pc]
    short2 = code[pc + 1]
    pc += 2

    i = short1 << 8 | short2
    if i >= 32768:
        i -= 65536
    vm_stack.push(i)
    return pc


def return_void(code, pc):
    # TODO
    print "return..."
    return pc


def putstatic(code, pc):
    # TODO
    indexbyte1 = code[pc]
    indexbyte2 = code[pc+1]
    pc += 2

    index = (indexbyte1 << 8) | indexbyte2
    value = vm_stack.pop()
    print "Put static: ", index, '=', value
    return pc


def invokestatic(code, pc):
    # TODO
    return pc


def aconst_null(code, pc):  # DONE
    vm_stack.push(None)
    return pc


def push_iconst(const):  # DONE
    vm_stack.push(const)


def iconst_m1(code, pc):  # DONE
    push_iconst(-1)
    return pc


def iconst_0(code, pc):  # DONE
    push_iconst(0)
    return pc


def iconst_1(code, pc):  # DONE
    push_iconst(1)
    return pc


def iconst_2(code, pc):  # DONE
    push_iconst(2)
    return pc


def iconst_3(code, pc):  # DONE
    push_iconst(3)
    return pc


def iconst_4(code, pc):  # DONE
    push_iconst(4)
    return pc


def iconst_5(code, pc):  # DONE
    push_iconst(5)
    return pc


def lconst_0(code, pc):  # DONE
    push_iconst(0)
    return pc


def lconst_1(code, pc):  # DONE
    push_iconst(1)
    return pc


def fconst_0(code, pc):  # DONE
    push_iconst(0.0)
    return pc


def fconst_1(code, pc):  # DONE
    push_iconst(1.0)
    return pc


def fconst_2(code, pc):  # DONE
    push_iconst(2.0)
    return pc


def dconst_0(code, pc):  # DONE
    push_iconst(0.0)
    return pc


def dconst_1(code, pc):  # DONE
    push_iconst(1.0)
    return pc


def ldc(code, pc):
    # TODO
    # Push item from run-time constant pool
    pass


def ldc_w(code, pc):
    # TODO
    # Push item from run-time constant pool (wide index)
    pass

def ldc2_w(code, pc):
    # TODO
    # Push long or double from run-time constant pool (wide index)
    return pc

def iload(code, pc):
    # TODO
    return pc

def lload(code, pc):
    # TODO
    return pc
def fload(code, pc):
    # TODO
    return pc
def dload(code, pc):
    # TODO
    return pc
def aload(code, pc):
    # TODO
    return pc
def iload_0(code, pc):
    # TODO
    return pc
def iload_1(code, pc):
    # TODO
    return pc
def iload_2(code, pc):
    # TODO
    return pc
def iload_3(code, pc):
    # TODO
    return pc
def lload_0(code, pc):
    # TODO
    return pc
def lload_1(code, pc):
    # TODO
    return pc
def lload_2(code, pc):
    # TODO
    return pc
def lload_3(code, pc):
    # TODO
    return pc
def fload_0(code, pc):
    # TODO
    return pc
def fload_1(code, pc):
    # TODO
    return pc
def fload_2(code, pc):
    # TODO
    return pc
def fload_3(code, pc):
    # TODO
    return pc
def dload_0(code, pc):
    # TODO
    return pc
def dload_1(code, pc):
    # TODO
    return pc
def dload_2(code, pc):
    # TODO
    return pc
def dload_3(code, pc):
    # TODO
    return pc
def aload_0(code, pc):
    # TODO
    return pc
def aload_1(code, pc):
    # TODO
    return pc
def aload_2(code, pc):
    # TODO
    return pc
def aload_3(code, pc):
    # TODO
    return pc
def iaload(code, pc):
    # TODO
    return pc
def laload(code, pc):
    # TODO
    return pc
def faload(code, pc):
    # TODO
    return pc
def daload(code, pc):
    # TODO
    return pc
def aaload(code, pc):
    # TODO
    return pc
def baload(code, pc):
    # TODO
    return pc
def caload(code, pc):
    # TODO
    return pc
def saload(code, pc):
    # TODO
    return pc
def istore(code, pc):
    # TODO
    return pc
def lstore(code, pc):
    # TODO
    return pc
def fstore(code, pc):
    # TODO
    return pc
def dstore(code, pc):
    # TODO
    return pc
def astore(code, pc):
    # TODO
    return pc
def istore_0(code, pc):
    # TODO
    return pc
def istore_1(code, pc):
    # TODO
    return pc
def istore_2(code, pc):
    # TODO
    return pc
def istore_3(code, pc):
    # TODO
    return pc
def lstore_0(code, pc):
    # TODO
    return pc
def lstore_1(code, pc):
    # TODO
    return pc
def lstore_2(code, pc):
    # TODO
    return pc
def lstore_3(code, pc):
    # TODO
    return pc
def fstore_0(code, pc):
    # TODO
    return pc
def fstore_1(code, pc):
    # TODO
    return pc
def fstore_2(code, pc):
    # TODO
    return pc
def fstore_3(code, pc):
    # TODO
    return pc
def dstore_0(code, pc):
    # TODO
    return pc
def dstore_1(code, pc):
    # TODO
    return pc
def dstore_2(code, pc):
    # TODO
    return pc
def dstore_3(code, pc):
    # TODO
    return pc
def astore_0(code, pc):
    # TODO
    return pc
def astore_1(code, pc):
    # TODO
    return pc
def astore_2(code, pc):
    # TODO
    return pc
def astore_3(code, pc):
    # TODO
    return pc
def iastore(code, pc):
    # TODO
    return pc
def lastore(code, pc):
    # TODO
    return pc
def fastore(code, pc):
    # TODO
    return pc
def dastore(code, pc):
    # TODO
    return pc
def aastore(code, pc):
    # TODO
    return pc
def bastore(code, pc):
    # TODO
    return pc
def castore(code, pc):
    # TODO
    return pc
def sastore(code, pc):
    # TODO
    return pc
def pop(code, pc):
    # TODO
    return pc
def pop2(code, pc):
    # TODO
    return pc
def dup(code, pc):
    # TODO
    return pc
def dup_x1(code, pc):
    # TODO
    return pc
def dup_x2(code, pc):
    # TODO
    return pc
def dup2(code, pc):
    # TODO
    return pc
def dup2_x1(code, pc):
    # TODO
    return pc
def dup2_x2(code, pc):
    # TODO
    return pc
def swap(code, pc):
    # TODO
    return pc
def iadd(code, pc):
    # TODO
    return pc
def ladd(code, pc):
    # TODO
    return pc
def fadd(code, pc):
    # TODO
    return pc
def dadd(code, pc):
    # TODO
    return pc
def isub(code, pc):
    # TODO
    return pc
def lsub(code, pc):
    # TODO
    return pc
def fsub(code, pc):
    # TODO
    return pc
def dsub(code, pc):
    # TODO
    return pc

def mul_number():
    v1 = vm_stack.pop()
    v2 = vm_stack.pop()
    vm_stack.push(v1 * v2)


def imul(code, pc):  # DONE
    mul_number()
    return pc


def lmul(code, pc):  # DONE
    mul_number()
    return pc


def fmul(code, pc):  # DONE
    mul_number()
    return pc


def dmul(code, pc):  # DONE
    mul_number()
    return pc


def idiv(code, pc):
    # TODO
    return pc
def ldiv(code, pc):
    # TODO
    return pc
def fdiv(code, pc):
    # TODO
    return pc
def ddiv(code, pc):
    # TODO
    return pc
def reminder_number():
    v1 = vm_stack.pop()
    v2 = vm_stack.pop()
    vm_stack.push(v1 % v2)

def irem(code, pc):
    # TODO
    
    return pc
def lrem(code, pc):
    # TODO
    return pc
def frem(code, pc):
    # TODO
    return pc
def drem(code, pc):
    # TODO
    return pc
def ineg(code, pc):
    # TODO
    return pc
def lneg(code, pc):
    # TODO
    return pc
def fneg(code, pc):
    # TODO
    return pc
def dneg(code, pc):
    # TODO
    return pc
def ishl(code, pc):
    # TODO
    return pc
def lshl(code, pc):
    # TODO
    return pc
def ishr(code, pc):
    # TODO
    return pc
def lshr(code, pc):
    # TODO
    return pc
def iushr(code, pc):
    # TODO
    return pc
def lushr(code, pc):
    # TODO
    return pc
def iand(code, pc):
    # TODO
    return pc
def land(code, pc):
    # TODO
    return pc
def ior(code, pc):
    # TODO
    return pc
def lor(code, pc):
    # TODO
    return pc
def ixor(code, pc):
    # TODO
    return pc
def lxor(code, pc):
    # TODO
    return pc
def iinc(code, pc):
    # TODO
    return pc
def i2l(code, pc):
    # TODO
    return pc
def i2f(code, pc):
    # TODO
    return pc
def i2d(code, pc):
    # TODO
    return pc
def l2f(code, pc):
    # TODO
    return pc
def l2f(code, pc):
    # TODO
    return pc
def l2d(code, pc):
    # TODO
    return pc
def f2i(code, pc):
    # TODO
    return pc
def f2l(code, pc):
    # TODO
    return pc
def f2d(code, pc):
    # TODO
    return pc
def d2i(code, pc):
    # TODO
    return pc
def d2l(code, pc):
    # TODO
    return pc
def d2f(code, pc):
    # TODO
    return pc
def i2b(code, pc):
    # TODO
    return pc
def i2c(code, pc):
    # TODO
    return pc
def i2s(code, pc):
    # TODO
    return pc
def lcmp(code, pc):
    # TODO
    return pc
def fcmpl(code, pc):
    # TODO
    return pc
def fcmpg(code, pc):
    # TODO
    return pc
def dcmpl(code, pc):
    # TODO
    return pc
def dcmpg(code, pc):
    # TODO
    return pc
def ifeq(code, pc):
    # TODO
    return pc
def ifne(code, pc):
    # TODO
    return pc
def iflt(code, pc):
    # TODO
    return pc
def ifge(code, pc):
    # TODO
    return pc
def ifgt(code, pc):
    # TODO
    return pc
def ifle(code, pc):
    # TODO
    return pc
def if_icmpeq(code, pc):
    # TODO
    return pc
def if_acmpne(code, pc):
    # TODO
    return pc
def if_icmplt(code, pc):
    # TODO
    return pc
def if_icmpge(code, pc):
    # TODO
    return pc
def if_icmpgt(code, pc):
    # TODO
    return pc
def if_icmple(code, pc):
    # TODO
    return pc
def if_acmpeq(code, pc):
    # TODO
    return pc
def if_acmpne(code, pc):
    # TODO
    return pc
def goto(code, pc):
    # TODO
    return pc
def jsr(code, pc):
    # TODO
    return pc
def ret(code, pc):
    # TODO
    return pc
def tableswitch(code, pc):
    # TODO
    return pc
def lookupswitch(code, pc):
    # TODO
    return pc
def ireturn(code, pc):
    # TODO
    return pc
def lreturn(code, pc):
    # TODO
    return pc
def freturn(code, pc):
    # TODO
    return pc
def dreturn(code, pc):
    # TODO
    return pc
def areturn(code, pc):
    # TODO
    return pc
def return_void(code, pc):
    # TODO
    return pc
def getstatic(code, pc):
    # TODO
    return pc
def putstatic(code, pc):
    # TODO
    return pc
def getfield(code, pc):
    # TODO
    return pc
def putfield(code, pc):
    # TODO
    return pc
def invokevirtual(code, pc):
    # TODO
    return pc
def invokespecial(code, pc):
    # TODO
    return pc
def invokestatic(code, pc):
    # TODO
    return pc
def invokeinterface(code, pc):
    # TODO
    return pc
def invokedynamic(code, pc):
    # TODO
    return pc
def new(code, pc):
    # TODO
    return pc
def newarray(code, pc):
    # TODO
    return pc
def anewarray(code, pc):
    # TODO
    return pc
def arraylength(code, pc):
    # TODO
    return pc
def athrow(code, pc):
    # TODO
    return pc
def checkcast(code, pc):
    # TODO
    return pc
def instanceof(code, pc):
    # TODO
    return pc
def monitorenter(code, pc):
    # TODO
    return pc
def monitorexit(code, pc):
    # TODO
    return pc
def wide(code, pc):
    # TODO
    return pc
def multianewarray(code, pc):
    # TODO
    return pc
def ifnull(code, pc):
    # TODO
    return pc
def ifnonnull(code, pc):
    # TODO
    return pc
def goto_w(code, pc):
    # TODO
    return pc
def jsr_w(code, pc):
    # TODO
    return pc
def breakpoint(code, pc):
    # TODO
    return pc
def impdep1(code, pc):
    # TODO
    return pc
def impdep2(code, pc):
    # TODO
    return pc

instruction_call_table = {
    0x00: nop,
    0x01: aconst_null,
    0x02: iconst_m1,
    0x03: iconst_0,
    0x04: iconst_1,
    0x05: iconst_2,
    0x06: iconst_3,
    0x07: iconst_4,
    0x08: iconst_5,
    0x09: lconst_0,
    0x10: lconst_1,
    0x0B: fconst_0,
    0x0C: fconst_1,
    0x0D: fconst_2,
    0x0E: dconst_0,
    0x0F: dconst_1,
    0x10: bipush,
    0x11: sipush,
    0x12: ldc,
    0x13: ldc_w,
    0x14: ldc2_w,
    0x15: iload,
    0x16: lload,
    0x17: fload,
    0x18: dload,
    0x19: aload,
    0x1A: iload_0,
    0x1B: iload_1,
    0x1C: iload_2,
    0x1D: iload_3,
    0x1E: lload_0,
    0x1F: lload_1,
    0x20: lload_2,
    0x21: lload_3,
    0x22: fload_0,
    0x23: fload_1,
    0x24: fload_2,
    0x25: fload_3,
    0x26: dload_0,
    0x27: dload_1,
    0x28: dload_2,
    0x29: dload_3,
    0x2A: aload_0,
    0x2B: aload_1,
    0x2C: aload_2,
    0x2D: aload_3,
    0x2E: iaload,
    0x2F: laload,
    0x30: faload,
    0x31: daload,
    0x32: aaload,
    0x33: baload,
    0x34: caload,
    0x35: saload,
    0x36: istore,
    0x37: lstore,
    0x38: fstore,
    0x39: dstore,
    0x3A: astore,
    0x3B: istore_0,
    0x3C: istore_1,
    0x3D: istore_2,
    0x3E: istore_3,
    0x3F: lstore_0,
    0x40: lstore_1,
    0x41: lstore_2,
    0x42: lstore_3,
    0x43: fstore_0,
    0x44: fstore_1,
    0x45: fstore_2,
    0x46: fstore_3,
    0x47: dstore_0,
    0x48: dstore_1,
    0x49: dstore_2,
    0x4A: dstore_3,
    0x4B: astore_0,
    0x4C: astore_1,
    0x4D: astore_2,
    0x4E: astore_3,
    0x4F: iastore,
    0x50: lastore,
    0x51: fastore,
    0x52: dastore,
    0x53: aastore,
    0x54: bastore,
    0x55: castore,
    0x56: sastore,
    0x57: pop,
    0x58: pop2,
    0x59: dup,
    0x5A: dup_x1,
    0x5B: dup_x2,
    0x5C: dup2,
    0x5D: dup2_x1,
    0x5E: dup2_x2,
    0x5F: swap,
    0x60: iadd,
    0x61: ladd,
    0x62: fadd,
    0x63: dadd,
    0x64: isub,
    0x65: lsub,
    0x66: fsub,
    0x67: dsub,
    0x68: imul,
    0x69: lmul,
    0x6A: fmul,
    0x6B: dmul,
    0x6C: idiv,
    0x6D: ldiv,
    0x6E: fdiv,
    0x6F: ddiv,
    0x70: irem,
    0x71: lrem,
    0x72: frem,
    0x73: drem,
    0x74: ineg,
    0x75: lneg,
    0x76: fneg,
    0x77: dneg,
    0x78: ishl,
    0x79: lshl,
    0x7A: ishr,
    0x7B: lshr,
    0x7C: iushr,
    0x7B: lushr,
    0x7E: iand,
    0x7F: land,
    0x80: ior,
    0x81: lor,
    0x82: ixor,
    0x83: lxor,
    0x84: iinc,
    0x85: i2l,
    0x86: i2f,
    0x87: i2d,
    0x88: l2f,
    0x89: l2f,
    0x8A: l2d,
    0x8B: f2i,
    0x8C: f2l,
    0x8D: f2d,
    0x8E: d2i,
    0x8F: d2l,
    0x90: d2f,
    0x91: i2b,
    0x92: i2c,
    0x93: i2s,
    0x94: lcmp,
    0x95: fcmpl,
    0x96: fcmpg,
    0x97: dcmpl,
    0x98: dcmpg,
    0x99: ifeq,
    0x9A: ifne,
    0x9B: iflt,
    0x9C: ifge,
    0x9D: ifgt,
    0x9E: ifle,
    0x9F: if_icmpeq,
    0xA0: if_acmpne,
    0xA1: if_icmplt,
    0xA2: if_icmpge,
    0xA3: if_icmpgt,
    0xA4: if_icmple,
    0xA5: if_acmpeq,
    0xA6: if_acmpne,
    0xA7: goto,
    0xA8: jsr,
    0xA9: ret,
    0xAA: tableswitch,
    0xAB: lookupswitch,
    0xAC: ireturn,
    0xAD: lreturn,
    0xAE: freturn,
    0xAF: dreturn,
    0xB0: areturn,
    0xB1: return_void,
    0xB2: getstatic,
    0xB3: putstatic,
    0xB4: getfield,
    0xB5: putfield,
    0xB6: invokevirtual,
    0xB7: invokespecial,
    0xB8: invokestatic,
    0xB9: invokeinterface,
    0xBA: invokedynamic,
    0xBB: new,
    0xBC: newarray,
    0xBD: anewarray,
    0xBE: arraylength,
    0xBF: athrow,
    0xC0: checkcast,
    0xC1: instanceof,
    0xC2: monitorenter,
    0xC3: monitorexit,
    0xC4: wide,
    0xC5: multianewarray,
    0xC6: ifnull,
    0xC7: ifnonnull,
    0xC8: goto_w,
    0xC9: jsr_w,
    0xCA: breakpoint,
    0xFE: impdep1,
    0xFF: impdep2,
    }


