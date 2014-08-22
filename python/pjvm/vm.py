#!/usr/bin/env python
# -*- coding: utf-8 -*-
from instruction_set import *

vm_stack = []


instruction_table = {
    0x00: ["nop", 0],
    0x01: ["aconst_null", 0],
    0x02: ["iconst_m1", 0],
    0x03: ["iconst_0", 0],
    0x04: ["iconst_1", 0],
    0x05: ["iconst_2", 0],
    0x06: ["iconst_3", 0],
    0x07: ["iconst_4", 0],
    0x08: ["iconst_5", 0],
    0x09: ["lconst_0", 0],
    0x10: ["lconst_1", 0],
    0x0B: ["fconst_0", 0],
    0x0C: ["fconst_1", 0],
    0x0D: ["fconst_2", 0],
    0x0E: ["dconst_0", 0],
    0x0F: ["dconst_1", 0],
    0x10: ["bipush", 1],
    0x11: ["sipush", 2],
    0x12: ["ldc", 1],
    0x13: ["ldc_w", 2],
    0x14: ["ldc2_w", 2],
    0x15: ["iload", 1],
    0x16: ["lload", 1],
    0x17: ["fload", 1],
    0x18: ["dload", 1],
    0x19: ["aload", 0],
    0x1A: ["iload_0", 0],
    0x1B: ["iload_1", 0],
    0x1C: ["iload_2", 0],
    0x1D: ["iload_3", 0],
    0x1E: ["lload_0", 0],
    0x1F: ["lload_1", 0],
    0x20: ["lload_2", 0],
    0x21: ["lload_3", 0],
    0x22: ["fload_0", 0],
    0x23: ["fload_1", 0],
    0x24: ["fload_2", 0],
    0x25: ["fload_3", 0],
    0x26: ["dload_0", 0],
    0x27: ["dload_1", 0],
    0x28: ["dload_2", 0],
    0x29: ["dload_3", 0],
    0x2A: ["aload_0", 0],
    0x2B: ["aload_1", 0],
    0x2C: ["aload_2", 0],
    0x2D: ["aload_3", 0],
    0x2E: ["iaload", 0],
    0x2F: ["laload", 0],
    0x30: ["faload", 0],
    0x31: ["daload", 0],
    0x32: ["aaload", 0],
    0x33: ["baload", 0],
    0x34: ["caload", 0],
    0x35: ["saload", 0],
    0x36: ["istore", 1],
    0x37: ["lstore", 1],
    0x38: ["fstore", 1],
    0x39: ["dstore", 1],
    0x3A: ["astore", 1],
    0x3B: ["istore_0", 0],
    0x3C: ["istore_1", 0],
    0x3D: ["istore_2", 0],
    0x3E: ["istore_3", 0],
    0x3F: ["lstore_0", 0],
    0x40: ["lstore_1", 0],
    0x41: ["lstore_2", 0],
    0x42: ["lstore_3", 0],
    0x43: ["fstore_0", 0],
    0x44: ["fstore_1", 0],
    0x45: ["fstore_2", 0],
    0x46: ["fstore_3", 0],
    0x47: ["dstore_0", 0],
    0x48: ["dstore_1", 0],
    0x49: ["dstore_2", 0],
    0x4A: ["dstore_3", 0],
    0x4B: ["astore_0", 0],
    0x4C: ["astore_1", 0],
    0x4D: ["astore_2", 0],
    0x4E: ["astore_3", 0],
    0x4F: ["iastore", 0],
    0x50: ["lastore", 0],
    0x51: ["fastore", 0],
    0x52: ["dastore", 0],
    0x53: ["aastore", 0],
    0x54: ["bastore", 0],
    0x55: ["castore", 0],
    0x56: ["sastore", 0],
    0x57: ["pop", 0],
    0x58: ["pop2", 0],
    0x59: ["dup", 0],
    0x5A: ["dup_x1", 0],
    0x5B: ["dup_x2", 0],
    0x5C: ["dup2", 0],
    0x5D: ["dup2_x1", 0],
    0x5E: ["dup2_x2", 0],
    0x5F: ["swap", 0],
    0x60: ["iadd", 0],
    0x61: ["ladd", 0],
    0x62: ["fadd", 0],
    0x63: ["dadd", 0],
    0x64: ["isub", 0],
    0x65: ["lsub", 0],
    0x66: ["fsub", 0],
    0x67: ["dsub", 0],
    0x68: ["imul", 0],
    0x69: ["lmul", 0],
    0x6A: ["fmul", 0],
    0x6B: ["dmul", 0],
    0x6C: ["idiv", 0],
    0x6D: ["ldiv", 0],
    0x6E: ["fdiv", 0],
    0x6F: ["ddiv", 0],
    0x70: ["irem", 0],
    0x71: ["lrem", 0],
    0x72: ["frem", 0],
    0x73: ["drem", 0],
    0x74: ["ineg", 0],
    0x75: ["lneg", 0],
    0x76: ["fneg", 0],
    0x77: ["dneg", 0],
    0x78: ["ishl", 0],
    0x79: ["lshl", 0],
    0x7A: ["ishr", 0],
    0x7B: ["lshr", 0],
    0x7C: ["iushr", 0],
    0x7B: ["lushr", 0],
    0x7E: ["iand", 0],
    0x7F: ["land", 0],
    0x80: ["ior", 0],
    0x81: ["lor", 0],
    0x82: ["ixor", 0],
    0x83: ["lxor", 0],
    0x84: ["iinc", 2],
    0x85: ["i2l", 0],
    0x86: ["i2f", 0],
    0x87: ["i2d", 0],
    0x88: ["l2f", 0],
    0x89: ["l2f", 0],
    0x8A: ["l2d", 0],
    0x8B: ["f2i", 0],
    0x8C: ["f2l", 0],
    0x8D: ["f2d", 0],
    0x8E: ["d2i", 0],
    0x8F: ["d2l", 0],
    0x90: ["d2f", 0],
    0x91: ["i2b", 0],
    0x92: ["i2c", 0],
    0x93: ["i2s", 0],
    0x94: ["lcmp", 0],
    0x95: ["fcmpl", 0],
    0x96: ["fcmpg", 0],
    0x97: ["dcmpl", 0],
    0x98: ["dcmpg", 0],
    0x99: ["ifeq", 2],
    0x9A: ["ifne", 2],
    0x9B: ["iflt", 2],
    0x9C: ["ifge", 2],
    0x9D: ["ifgt", 2],
    0x9E: ["ifle", 2],
    0x9F: ["if_icmpeq", 2],
    0xA0: ["if_acmpne", 2],
    0xA1: ["if_icmplt", 2],
    0xA2: ["if_icmpge", 2],
    0xA3: ["if_icmpgt", 2],
    0xA4: ["if_icmple", 2],
    0xA5: ["if_acmpeq", 2],
    0xA6: ["if_acmpne", 2],
    0xA7: ["goto", 2],
    0xA8: ["jsr", 2],
    0xA9: ["ret", 1],
    0xAA: ["tableswitch", 3.5],
    0xAB: ["lookupswitch", 3.5],
    0xAC: ["ireturn", 0],
    0xAD: ["lreturn", 0],
    0xAE: ["freturn", 0],
    0xAF: ["dreturn", 0],
    0xB0: ["areturn", 0],
    0xB1: ["return", 0],
    0xB2: ["getstatic", 2],
    0xB3: ["putstatic", 2],
    0xB4: ["getfield", 2],
    0xB5: ["putfield", 2],
    0xB6: ["invokevirtual", 2],
    0xB7: ["invokespecial", 2],
    0xB8: ["invokestatic", 2],
    0xB9: ["invokeinterface", 4],
    0xBA: ["invokedynamic", 4],
    0xBB: ["new", 2],
    0xBC: ["newarray", 1],
    0xBD: ["anewarray", 2],
    0xBE: ["arraylength", 0],
    0xBF: ["athrow", 0],
    0xC0: ["checkcast", 2],
    0xC1: ["instanceof", 2],
    0xC2: ["monitorenter", 0],
    0xC3: ["monitorexit", 0],
    0xC4: ["wide", 3.5],
    0xC5: ["multianewarray", 3],
    0xC6: ["ifnull", 2],
    0xC7: ["ifnonnull", 2],
    0xC8: ["goto_w", 4],
    0xC9: ["jsr_w", 4],
    0xCA: ["breakpoint", 0],
    0xFE: ["impdep1", 0],
    0xFF: ["impdep2", 0]
    }


def code_to_int(code_string):
    code = []
    i = 0
    while(i < len(code)):
        code.append(int(code_string[i: i + 2], 16))
        i += 2
    return code


def run(code):
    pc = 0
    while(pc < len(code)):
        instruction = code[i]
        pc += 1
        pc = call_instruction(instruction, code, pc)


def call_instruction(ins, code, pc):
    return instruction_call_table[ins](code, pc)


def instructiones(info):
    s = 0
    while(True):
        if s == len(info):
            break
        instruction = int(info[s: s + 1*2], 16)
        s += 1*2
        name, jump = instruction_table[instruction]
        if jump != 0:
            paras = []
            for i in range(jump):
                para = str(int(info[s: s + 1*2], 16))
                paras.append(para)
                s += 1*2
            yield name+" "+"".join(paras)
        else:
            yield name


def main():
    # print "\n".join(instructiones("2ab7000cb1"))
    run(code_to_int('113039b3000c10f6b3000e112710b30010b1'))
    # instructiones("00010001000000052ab7000cb100000002000e00000006000100000003000f0000000c000100000005001000110000")

if __name__ == '__main__':
    main()
