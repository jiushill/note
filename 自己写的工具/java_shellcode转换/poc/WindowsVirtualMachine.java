package sun.tools.attach;

import java.io.IOException;

public class WindowsVirtualMachine {
    public WindowsVirtualMachine() {
    }

    static native void enqueue(long var0, byte[] var2, String var3, String var4, Object... var5) throws IOException;

    static native long openProcess(int var0) throws IOException;

    public static void run(byte[] buf)throws IOException {
        System.loadLibrary("attach");
        enqueue(-1L, buf, "test", "test");
    }
}