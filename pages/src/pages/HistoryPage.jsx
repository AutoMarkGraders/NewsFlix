import { useState } from 'react';
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { Button } from "@/components/ui/button";
import { Combobox } from '@/components/ui/Combobox';

import './HistoryPage.css';

const HistoryPage = () => {
    const [showReelPlayer, setShowReelPlayer] = useState(false);

    
    return (
    <div>
        <div id='top'>

            <div className='filter'>
            <h2>Filter by Language</h2>
            <ToggleGroup type="multiple" variant="outline">
                <ToggleGroupItem value="en">
                    English
                </ToggleGroupItem>
                <ToggleGroupItem value="hi">
                    हिन्दी
                </ToggleGroupItem>
                <ToggleGroupItem value="ml">
                    മലയാളം
                </ToggleGroupItem>
            </ToggleGroup>
            </div>

            <div className='filter'>
            <h2>Filter by Category</h2>
            <Combobox />
            </div>

            <Button id='searchButton' onClick={() => alert('clicked')}>Search</Button>

        </div>
    </div>
    )
}

export default HistoryPage