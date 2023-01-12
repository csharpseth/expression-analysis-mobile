import { AppProvider } from "./app/contexts/AppContext";
import Navigation from "./app/views/components/Navigation";

export default function App() {
	return (
		<AppProvider>
			<Navigation />
		</AppProvider>
	);
}
