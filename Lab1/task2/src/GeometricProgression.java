import java.util.ArrayList;
import java.util.List;

public class GeometricProgression {
    private static List<GeometricProgression> instances = new ArrayList<>();
    private static int counter = 0; // static variable to count the instances
    private int b; // first term of geometric progression
    private int q; // common ratio

    public static String printAllInstances() {
        System.out.println("\nInformation about all instances:");
        for (GeometricProgression instance : instances) {
            System.out.println(instance);
        }
        return "Existing instances: " + counter;
    }

    public GeometricProgression(int b, int q) {
        this.b = b;
        this.q = q;
        instances.add(this);
        counter++;
    }

    public int getB() {
        return b;
    }

    public void setB(int b) {
        this.b = b;
    }

    public int getQ() {
        return q;
    }

    public void setQ(int q) {
        this.q = q;
    }

    public int firstElement() {
        return b;
    }

    public int nElement(int n) {
        return (int) (b * Math.pow(q, n - 1));
    }

    public List<Integer> sequenceFromKToM(int k, int m) {
        List<Integer> sequence = new ArrayList<>();
        for (int i = k; i <= m; i++) {
            sequence.add(nElement(i));
        }
        return sequence;
    }

    public void changeParameters(int newB, int newQ) {
        b = newB;
        q = newQ;
    }

    @Override
    public String toString() {
        List<Integer> sequence = sequenceFromKToM(1, 7);
        String elements = String.join(", ", sequence.stream().map(Object::toString).toArray(String[]::new));
        return String.format("& %d, %d: {%s ...}", b, q, elements);
    }
}
