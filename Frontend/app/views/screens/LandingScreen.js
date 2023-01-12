import { Text, View, StyleSheet } from 'react-native';

function LandingScreen() {
    return (
        <View style={styles.container}>
            <Text>Hello World!</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    }
})

export default LandingScreen;