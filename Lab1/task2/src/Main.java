public class Main {
    public static void main(String[] args) {
        GeometricProgression gp1 = new GeometricProgression(1, 4);
        System.out.println("PROGRESSION 1");
        System.out.println("First element of progression1 is " + gp1.firstElement());
        System.out.println(gp1);

        GeometricProgression gp2 = new GeometricProgression(3, 3);
        System.out.println("\nPROGRESSION 2");
        System.out.println("Fifth element of progression2 is " + gp2.nElement(5));
        System.out.println(gp2);

        gp2.changeParameters(7, 2);
        System.out.println("\nUPDATED PROGRESSION 2");
        System.out.println(gp2);
        System.out.println("\n" + GeometricProgression.printAllInstances());
    }
}