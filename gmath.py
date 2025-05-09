import moderngl
import struct

version = "0.54"


class gMath:
    def __init__(self, shadersPath):

        self.ctx = moderngl.create_standalone_context()
        self.path = shadersPath

        self.addComputeShader = None
        self.subComputeShader = None
        self.multComputeShader = None
        self.divComputeShader = None

        self.initShader()
        self.initComputeProgram()
        self.initBuffer()


    def initShader(self):

        with open(f"{self.path}/add.comp") as f:
            self.addComputeShader = f.read()

        with open(f"{self.path}/sub.comp") as f:
            self.subComputeShader = f.read()

        with open(f"{self.path}/mult.comp") as f:
            self.multComputeShader = f.read()

        with open(f"{self.path}/div.comp") as f:
            self.divComputeShader = f.read()


    def initComputeProgram(self):

        self.addComputeProgram = self.ctx.compute_shader(self.addComputeShader)
        self.subComputeProgram = self.ctx.compute_shader(self.subComputeShader)
        self.multComputeProgram = self.ctx.compute_shader(self.multComputeShader)
        self.divComputeProgram = self.ctx.compute_shader(self.divComputeShader)


    def initBuffer(self):
        self.addBuffer = self.ctx.buffer(reserve=8)
        self.addBuffer.bind_to_storage_buffer(0)

        self.subBuffer = self.ctx.buffer(reserve=8)
        self.subBuffer.bind_to_storage_buffer(1)

        self.multBuffer = self.ctx.buffer(reserve=8)
        self.multBuffer.bind_to_storage_buffer(2)

        self.divBuffer = self.ctx.buffer(reserve=8)
        self.divBuffer.bind_to_storage_buffer(3)


    def clear(self):

        self.addComputeShader = None
        self.subComputeShader = None
        self.multComputeShader = None
        self.divComputeShader = None

        self.addComputeProgram = None
        self.subComputeProgram = None
        self.multComputeProgram = None
        self.divComputeProgram = None


    def add(self, x, y):
        self.addComputeProgram['x'] = x
        self.addComputeProgram['y'] = y
        
        self.addComputeProgram.run()

        return struct.unpack('d',self.addBuffer.read())[0]
    
    def subtract(self, x, y):
        self.subComputeProgram['x'] = x
        self.subComputeProgram['y'] = y
        
        self.subComputeProgram.run()

        return struct.unpack('d',self.subBuffer.read())[0]
    
    def multiply(self, x, y):
        self.multComputeProgram['x'] = x
        self.multComputeProgram['y'] = y
        
        self.multComputeProgram.run()

        return struct.unpack('d',self.multBuffer.read())[0]
    
    def divide(self, x, y):
        self.divComputeProgram['x'] = x
        self.divComputeProgram['y'] = y
        
        self.divComputeProgram.run()

        return struct.unpack('d',self.divBuffer.read())[0]


if __name__ == "__main__":
    print(f"gMath: v{version}")