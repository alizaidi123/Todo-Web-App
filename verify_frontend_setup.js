/**
 * Script to verify frontend setup
 */
const fs = require('fs');
const path = require('path');

console.log('Verifying frontend setup...');

// Check if the chat page exists
const chatPagePath = path.join(__dirname, 'frontend', 'app', 'chat', 'page.tsx');
if (fs.existsSync(chatPagePath)) {
    console.log('✓ Chat page exists');

    // Read the file to verify it contains expected content
    const chatPageContent = fs.readFileSync(chatPagePath, 'utf8');
    if (chatPageContent.includes('@chatscope/chat-ui-kit-react') &&
        chatPageContent.includes('ChatContainer') &&
        chatPageContent.includes('/api/chat/message')) {
        console.log('✓ Chat page contains expected ChatKit components and API calls');
    } else {
        console.log('⚠️  Chat page may be missing expected components');
    }
} else {
    console.log('❌ Chat page does not exist');
}

// Check if the chat layout exists
const chatLayoutPath = path.join(__dirname, 'frontend', 'app', 'chat', 'layout.tsx');
if (fs.existsSync(chatLayoutPath)) {
    console.log('✓ Chat layout exists');
} else {
    console.log('❌ Chat layout does not exist');
}

// Check if package.json has required dependencies
const packageJsonPath = path.join(__dirname, 'frontend', 'package.json');
if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const requiredDeps = ['@chatscope/chat-ui-kit-react', '@chatscope/chat-ui-kit-styles', 'axios'];

    for (const dep of requiredDeps) {
        if (packageJson.dependencies && packageJson.dependencies[dep]) {
            console.log(`✓ Dependency ${dep} is present`);
        } else {
            console.log(`❌ Dependency ${dep} is missing`);
        }
    }
} else {
    console.log('❌ package.json not found');
}

// Check if the main page has the chat button
const mainPagePath = path.join(__dirname, 'frontend', 'app', 'page.tsx');
if (fs.existsSync(mainPagePath)) {
    const mainPageContent = fs.readFileSync(mainPagePath, 'utf8');
    if (mainPageContent.includes('Chat with AI') && mainPageContent.includes('/chat')) {
        console.log('✓ Main page contains Chat with AI button');
    } else {
        console.log('⚠️  Main page may be missing Chat with AI button');
    }
} else {
    console.log('❌ Main page not found');
}

console.log('\nFrontend verification complete!');